from django.contrib import admin
from gt.service.models import Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    classes = ('collapse-entry', 'expand-first', )

    def get_queryset(self, request):
        qs = super(ServiceInline, self).get_queryset(request)
        qs = Service.objects.order_by('-service_date')

        return qs
