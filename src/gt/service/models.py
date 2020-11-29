from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.formats import localize
from django.utils.translation import gettext_lazy as _
from gt.vehicle.models import Vehicle


class Service(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        null=False,
        on_delete=models.CASCADE,
    )
    work_description = models.TextField(
        null=False,
        verbose_name=_('Service description')
    )
    remarks = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Remarks')
    )
    travel_distance = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Travel distance in kilometers'),
        validators=[MinValueValidator(0)]
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Service cost'),
        validators=[MinValueValidator(0)]
    )
    service_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        verbose_name=_('Service creation date')
    )
    creation_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        verbose_name=_('Entry creation date'),
        editable=False
    )

    def __str__(self) -> str:
        return "Km: {} - {}".format(self.travel_distance,
                                    localize(self.service_date))

    class Meta:
        db_table = 'service'
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
