from datetime import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils import timezone
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from gt.vehicle.pdf import vehicles_pdf
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
    inlines = (ServiceInline, VehicleOwnershipInline,)
    list_display = ('plate_number', 'manufacturer', 'last_service_date', 'total_cost', 'total_damage_cost', 'last_travel_distance')
    search_fields = ('plate_number', 'manufacturer',
                     'vehicle_identification_number',
                     'vehicleownership__vehicle_owner__full_name',
                     'vehicleownership__vehicle_owner__phone1')
    readonly_fields = ('total_cost', 'total_damage_cost',
                       'last_travel_distance')
    fieldsets = (
        (_('Client'), {
            'fields': ('plate_number', 'manufacturer', 'color',
                       'vehicle_identification_number', 'engine_number', 'engine_oil',
                       'construction_year', 'last_travel_distance',
                       'total_cost', 'total_damage_cost'),
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

    @admin.display(description=_('Last service date'),
                   ordering='last_service_date')
    def last_service_date(self, obj):
        value = obj.last_service_date
        return timezone.localtime(value).date() if value else None

    @admin.display(description=_('Travel distance (km)'))
    def last_travel_distance(self, obj):
        return obj.last_service_travel_distance

    def total_cost(self, obj):
        return obj.total_cost

    def total_damage_cost(self, obj):
        return obj.total_damage_cost

    def get_urls(self):
        custom = [
            path('<int:object_id>/export-pdf/',
                 self.admin_site.admin_view(self.export_pdf_view),
                 name='vehicle_vehicle_export_pdf'),
        ]
        return custom + super().get_urls()

    def export_pdf_view(self, request, object_id):
        vehicle = get_object_or_404(Vehicle, pk=object_id)
        return self._pdf_response([vehicle], vehicle.plate_number.lower())

    def export_pdf(self, _, queryset):
        if not queryset.count():
            return
        return self._pdf_response(queryset, 'vehicles')

    @staticmethod
    def _pdf_response(vehicles, name):
        filename = "{}-{}.pdf".format(
            name, datetime.now().strftime('%Y%m%d-%H%M'))
        response = HttpResponse(vehicles_pdf(vehicles),
                                content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    export_pdf.short_description = "Export to PDF"
    actions = [export_pdf]


@admin.register(VehicleOwner)
class VehicleOwner(ModelAdmin):
    list_display = ('full_name', 'address', 'phone1', 'phone2')
    search_fields = ('full_name', 'phone1',
                     'vehicleownership__vehicle__plate_number')
