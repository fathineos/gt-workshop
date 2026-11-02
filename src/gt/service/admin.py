from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone
from gt.service.models import Service


class ServiceInlineForm(forms.ModelForm):
    """Edit only the date of a service; the time of day is kept behind the
    scenes (existing time is preserved, new entries get the current time)."""

    service_date = forms.DateField(
        label=Service._meta.get_field('service_date').verbose_name,
        widget=AdminDateWidget,
        initial=timezone.localdate,
    )

    class Meta:
        model = Service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = self.initial.get('service_date')
        if isinstance(value, datetime):
            self.initial['service_date'] = timezone.localtime(value).date()

    def clean_service_date(self):
        day = self.cleaned_data['service_date']
        existing = self.instance.service_date if self.instance.pk else None
        local = timezone.localtime(existing if existing else timezone.now())
        if existing and local.date() == day:
            return existing
        return timezone.make_aware(datetime.combine(day, local.time()))


class ServiceInline(admin.TabularInline):
    model = Service
    form = ServiceInlineForm
    extra = 0
    classes = ('collapse-entry', 'expand-first', )
    fields = ('service_date', 'work_description', 'cost', 'damage', 'workshop')

    class Media:
        css = {'all': ('service/service_inline_mobile.css',)}
        js = ('service/add_service_top.js',
              'service/service_inline_labels.js')

    def get_queryset(self, request):
        qs = super(ServiceInline, self).get_queryset(request)
        qs = Service.objects.order_by('-service_date')

        return qs
