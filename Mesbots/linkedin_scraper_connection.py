from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import logging
import os

# Configuration du logging
logging.basicConfig(filename='linkedin_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def wait_for_element(driver, by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_and_click(driver, by, value, timeout=10, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            driver.execute_script("arguments[0].click();", element)
            return True
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            if attempt == retries - 1:
                logging.error(f"Erreur après {retries} tentatives : {str(e)}")
                return False
        time.sleep(random.uniform(0.5, 1.5))

def login_to_linkedin(driver, email, password):
    logging.info("Accès à la page de connexion LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(1.0, 2.0))

    logging.info("Tentative de connexion...")
    email_element = wait_for_element(driver, By.ID, "username")
    email_element.send_keys(email)

    password_element = wait_for_element(driver, By.ID, "password")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    logging.info("Attente de la page d'accueil...")
    wait_for_element(driver, By.ID, "global-nav")
    time.sleep(random.uniform(2.0, 3.0))

def check_login_status(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
        return True
    except:
        return False

def wait_for_page_load(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        return False

def take_screenshot(driver, filename):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/{filename}")

def search_profiles(driver, keywords, max_profiles, max_scroll):
    logging.info(f"Accès à la page de recherche pour '{keywords}'...")
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
    driver.get(search_url)

    logging.info("Attente des résultats de recherche...")
    wait_for_element(driver, By.CLASS_NAME, "search-results-container")
    time.sleep(random.uniform(1.0, 2.0))

    profile_urls = set()
    scroll_count = 0

    while scroll_count < max_scroll and len(profile_urls) < max_profiles:
        logging.info(f"Défilement {scroll_count + 1}/{max_scroll}...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1.5, 2.5))

        logging.info("Recherche des liens de profil...")
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
        new_urls = {link.get_attribute('href') for link in links if '/in/' in link.get_attribute('href')}
        profile_urls.update(new_urls)

        logging.info(f"Profils trouvés : {len(profile_urls)}")

        if len(profile_urls) >= max_profiles:
            break

        scroll_count += 1
        time.sleep(random.uniform(1.0, 2.0))

    return list(profile_urls)[:max_profiles]

def send_connection_request(driver, profile_url):
    driver.get(profile_url)
    if not wait_for_page_load(driver):
        logging.error("La page n'a pas fini de charger.")
        return

    try:
        logging.info(f"Accès au profil : {profile_url}")
        time.sleep(random.uniform(1.0, 2.0))

        selectors = [
            "//button[contains(@aria-label, 'se connecter')]",
            "//button[contains(@class, 'artdeco-button--primary')]",
            "//button[contains(text(), 'Se connecter')]",
            "//button[contains(@class, 'pvs-profile-actions__action')]",
            "//div[contains(@class, 'pvs-profile-actions')]//button",
            "//button[contains(@class, 'artdeco-button--2')]"
        ]

        time.sleep(random.uniform(1.0, 2.0))

        for selector in selectors:
            if wait_and_click(driver, By.XPATH, selector):
                logging.info("Bouton de connexion trouvé et cliqué.")
                break
        else:
            logging.warning("Aucun bouton de connexion trouvé.")
            take_screenshot(driver, f"error_{int(time.time())}.png")
            return

        time.sleep(random.uniform(0.5, 1.5))

        if wait_and_click(driver, By.XPATH, "//button[contains(@aria-label, 'Envoyer maintenant')]"):
            logging.info("Demande de connexion envoyée.")
        else:
            logging.warning("Bouton d'envoi non trouvé ou non cliquable.")

        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        logging.error(f"Une erreur est survenue lors de l'envoi de la demande de connexion : {str(e)}")

def scrape_and_connect(keywords, email, password, max_profiles=10, max_scroll=3):
    driver = setup_driver()

    try:
        login_to_linkedin(driver, email, password)
        profiles = search_profiles(driver, keywords, max_profiles, max_scroll)
        for profile in profiles:
            if not check_login_status(driver):
                logging.info("Session expirée, reconnexion...")
                login_to_linkedin(driver, email, password)
            send_connection_request(driver, profile)
            time.sleep(random.uniform(10, 20))  # Pause plus courte entre chaque profil

    except Exception as e:
        logging.error(f"Une erreur est survenue : {str(e)}")
    finally:
        logging.info("Fermeture du navigateur...")
        driver.quit()

if __name__ == "__main__":
    email = "yannjuniorsim@gmail.com"  # Remplacez par votre email LinkedIn
    password = "Lavitesse123*"  # Remplacez par votre mot de passe LinkedIn
    keywords = "MydigitalSchool"  # Modifiez selon vos besoins
    max_profiles = 10

    try:
        scrape_and_connect(keywords, email, password, max_profiles)
    except KeyboardInterrupt:
        logging.info("\nScript interrompu par l'utilisateur.")
    except Exception as e:
        logging.error(f"Une erreur inattendue est survenue : {str(e)}")
