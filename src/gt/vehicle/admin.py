from django.contrib import admin
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from gt.vehicle.models import Vehicle, VehicleOwner, VehicleOwnership
from gt.service.admin import ServiceInline


admin.site.disable_action('delete_selected')


class ModelAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_delete': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)


class VehicleOwnershipInline(admin.StackedInline):
    model = VehicleOwnership
    autocomplete_fields = ['vehicle_owner']
    extra = 0


@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    actions = []
    inlines = (ServiceInline, VehicleOwnershipInline,)
    list_display = ('plate_number', 'manufacturer', 'last_service_date')
    search_fields = ('plate_number', 'manufacturer',
                     'vehicle_identification_number',
                     'vehicleownership__vehicle_owner__full_name',
                     'vehicleownership__vehicle_owner__phone1')
    fieldsets = (
        (_('Client'), {
            'fields': ('plate_number', 'manufacturer', 'color',
                       'vehicle_identification_number', 'engine_number',
                       'construction_year'),
            'classes': ('baton-tabs-init', 'baton-tab-inline-service',
                        'baton-tab-inline-vehicleownership'),
        }),
    )

    def get_queryset(self, request):
        qs = super(VehicleAdmin, self).get_queryset(request)
        qs = Vehicle.objects.annotate(
            last_service_date=Max('service__service_date')
        ).order_by(
            '-last_service_date'
        )

        return qs

    def last_service_date(self, obj):
        return obj.last_service_date


@admin.register(VehicleOwner)
class VehicleOwner(ModelAdmin):
    list_display = ('full_name', 'address', 'phone1', 'phone2')
    search_fields = ('full_name', 'phone1',
                     'vehicleownership__vehicle__plate_number')
