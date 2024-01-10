from typing import Optional
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    plate_number = models.CharField(
        null=False,
        max_length=7,
        verbose_name=_('Vehicle plate number')
    )
    manufacturer = models.CharField(
        null=False,
        max_length=64,
        verbose_name=_('Vehicle manufacturer')
    )
    color = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_('Vehicle color')
    )
    vehicle_identification_number = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name=_('Vehicle identification number')
    )
    engine_number = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_('Engine number')
    )
    engine_oil = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_('Engine oil')
    )
    construction_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900),
                    MaxValueValidator(2100)],
        verbose_name=_('Construction year')
    )
    purchage_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Purchage date')
    )
    creation_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        verbose_name=_('Entry creation date'),
        editable=False
    )

    def __str__(self) -> str:
        return self.plate_number

    @property
    def total_service_cost(self) -> float:
        return float(self.service_set.aggregate(models.Sum('cost'))['cost__sum'])

    @property
    def last_service_travel_distance(self) -> Optional[int]:
        last_service = self.service_set.latest('service_date')
        return last_service.travel_distance if last_service else None


    class Meta:
        db_table = 'vehicle'
        unique_together = ('id', 'plate_number')
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')


class VehicleOwner(models.Model):
    full_name = models.CharField(
        null=False,
        max_length=100,
        verbose_name=_('Full name')
    )
    address = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Address')
    )
    phone1 = models.CharField(
        null=False,
        max_length=10,
        verbose_name=_('Primary phone')
    )
    phone2 = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        verbose_name=_('Secondary phone')
    )
    vehicles = models.ManyToManyField(
        Vehicle,
        through='VehicleOwnership'
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = 'vehicle_owner'
        verbose_name = _('Vehicle owner')
        verbose_name_plural = _('Vehicle owners')


class VehicleOwnership(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )
    vehicle_owner = models.ForeignKey(
        VehicleOwner,
        on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{} -> {}'.format(self.vehicle_owner.full_name,
                                 self.vehicle)

    class Meta:
        db_table = 'vehicle_ownership'
        verbose_name = _('Vehicle ownership')
        verbose_name_plural = _('Vehicle ownerships')
        unique_together = ('vehicle_id', 'vehicle_owner_id')
