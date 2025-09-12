from django.contrib import admin

# Register your models here.
# main/admin.py

from django.contrib import admin
from .models import Project, Skill, Contact, Blog, About

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Contact)
admin.site.register(Blog)
admin.site.register(About)

