from csv import writer
from datetime import datetime
from io import BytesIO, StringIO
from typing import Tuple
from zipfile import ZipFile
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from gt.vehicle.models import Vehicle, VehicleOwner, VehicleOwnership
from gt.service.admin import ServiceInline
from gt.service.models import Service


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
    list_display = ('plate_number', 'manufacturer', 'last_service_date', 'total_service_cost', 'last_service_travel_distance')
    search_fields = ('plate_number', 'manufacturer',
                     'vehicle_identification_number',
                     'vehicleownership__vehicle_owner__full_name',
                     'vehicleownership__vehicle_owner__phone1')
    fieldsets = (
        (_('Client'), {
            'fields': ('plate_number', 'manufacturer', 'color',
                       'vehicle_identification_number', 'engine_number', 'engine_oil',
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

    def export_csv(self, _, queryset):
        if not queryset.count():
            return

        csv_files = [
            self._generate_vehicle_csv(v) for v in queryset for v in queryset.all()
        ]
        filename = "{}.{}".format(
            datetime.now().strftime('%Y%m%d-%H%m'),
            'zip'
        )
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zipf:
            for file_name, csv_file in csv_files:
                zipf.writestr(file_name, csv_file.getvalue())
                csv_file.close()

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    @classmethod
    def _generate_vehicle_csv(cls, vehicle) -> Tuple[str, StringIO]:
        filename = "{}-{}.{}".format(
            vehicle.plate_number.lower(),
            datetime.now().strftime('%Y%m%d-%H%m'),
            'csv'
        )
        csv = StringIO()
        csv_writer = writer(csv)
        headers = []
        for field in Service._meta.fields:
            headers.append(field.verbose_name)
        csv_writer.writerow(headers)

        for service in vehicle.service_set.order_by('-service_date'):
            row = []
            for field in Service._meta.fields:
                value = getattr(service, field.name)
                if callable(value):
                    value = value()
                row.append(value)
            csv_writer.writerow(row)

        return (filename, csv)


    export_csv.short_description = "Export to CSV"
    actions = [export_csv]


@admin.register(VehicleOwner)
class VehicleOwner(ModelAdmin):
    list_display = ('full_name', 'address', 'phone1', 'phone2')
    search_fields = ('full_name', 'phone1',
                     'vehicleownership__vehicle__plate_number')
