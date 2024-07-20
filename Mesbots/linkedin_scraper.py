from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random


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


def login_to_linkedin(driver, email, password):
    print("Accès à la page de connexion LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2.0, 4.0))

    print("Tentative de connexion...")
    email_element = wait_for_element(driver, By.ID, "username")
    email_element.send_keys(email)

    password_element = wait_for_element(driver, By.ID, "password")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    print("Attente de la page d'accueil...")
    wait_for_element(driver, By.ID, "global-nav")
    time.sleep(random.uniform(3.0, 5.0))


def search_profiles(driver, keywords, max_profiles, max_scroll):
    print(f"Accès à la page de recherche pour '{keywords}'...")
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
    driver.get(search_url)

    print("Attente des résultats de recherche...")
    wait_for_element(driver, By.CLASS_NAME, "search-results-container")
    time.sleep(random.uniform(2.0, 4.0))

    print(f"Titre de la page : {driver.title}")
    print(f"Contenu partiel de la page : {driver.find_element(By.TAG_NAME, 'body').text[:500]}")

    profile_urls = set()
    scroll_count = 0

    while scroll_count < max_scroll and len(profile_urls) < max_profiles:
        print(f"Défilement {scroll_count + 1}/{max_scroll}...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2.5, 4.0))

        print("Recherche des liens de profil...")
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
        new_urls = {link.get_attribute('href') for link in links if '/in/' in link.get_attribute('href')}
        profile_urls.update(new_urls)

        print(f"Profils trouvés : {len(profile_urls)}")

        if len(profile_urls) >= max_profiles:
            break

        scroll_count += 1
        time.sleep(random.uniform(1.5, 3.0))

    return list(profile_urls)[:max_profiles]


def scrape_linkedin_profiles(keywords, email, password, max_profiles=10, max_scroll=3):
    driver = setup_driver()

    try:
        login_to_linkedin(driver, email, password)
        profiles = search_profiles(driver, keywords, max_profiles, max_scroll)
        return profiles

    except TimeoutException:
        print("Timeout lors du chargement d'un élément.")
    except NoSuchElementException:
        print("Un élément n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")
    finally:
        print("Fermeture du navigateur...")
        driver.quit()

    return []


if __name__ == "__main__":
    email = "yannjuniorsim@gmail.com"  # Remplacez par votre email LinkedIn
    password = "Lavitesse123*"  # Remplacez par votre mot de passe LinkedIn
    keywords = "ensimag"  # Modifiez selon vos besoins
    max_profiles = 10

    profiles = scrape_linkedin_profiles(keywords, email, password, max_profiles)

    print("\nURLs des profils LinkedIn trouvés :")
    for url in profiles:
        print(url)

    print(f"\nNombre total de profils trouvés : {len(profiles)}")