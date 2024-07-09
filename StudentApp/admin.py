from django.contrib import admin
from StudentApp.models import Company, School, Specialty, Program, Subject, Student , Mission, Comment
from Accounts.models import User
admin.site.register(School)
admin.site.register(Specialty)
admin.site.register(Program)
admin.site.register(Subject)
admin.site.register(Student)

admin.site.register(Company)
admin.site.register(Mission)
admin.site.register(Comment)
admin.site.register(User)