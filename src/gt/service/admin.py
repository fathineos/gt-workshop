from django.contrib import admin
from gt.service.models import Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    classes = ('collapse-entry', 'expand-first', )
