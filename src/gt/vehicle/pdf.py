from pathlib import Path
from typing import Iterable

from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext as _
from fpdf import FPDF
from fpdf.enums import XPos, YPos

from gt.vehicle.models import Vehicle

FONT_DIR = Path(__file__).parent / 'fonts'
FONT = 'DejaVu'


def _new_pdf() -> FPDF:
    pdf = FPDF(orientation='L', format='A4')
    pdf.add_font(FONT, '', str(FONT_DIR / 'DejaVuSans.ttf'))
    pdf.add_font(FONT, 'B', str(FONT_DIR / 'DejaVuSans-Bold.ttf'))
    pdf.set_auto_page_break(True, margin=12)
    return pdf


def _line(pdf: FPDF, text: str, bold: bool = False, size: int = 10) -> None:
    pdf.set_font(FONT, 'B' if bold else '', size)
    pdf.cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def _add_vehicle(pdf: FPDF, vehicle: Vehicle) -> None:
    pdf.add_page()
    _line(pdf, f'{vehicle.plate_number} - {vehicle.manufacturer}', True, 16)
    pdf.ln(2)

    details = (
        ('color', vehicle.color),
        ('vehicle_identification_number',
         vehicle.vehicle_identification_number),
        ('engine_number', vehicle.engine_number),
        ('engine_oil', vehicle.engine_oil),
        ('construction_year', vehicle.construction_year),
    )
    for name, value in details:
        if value:
            label = Vehicle._meta.get_field(name).verbose_name
            _line(pdf, f'{label}: {value}')
    pdf.ln(3)

    headers = (
        _('Service creation date'), _('Service description'), _('Remarks'),
        _('Travel distance in kilometers'), _('Service cost'), _('Damage?'),
        _('Workshop name'),
    )
    widths = (24, 80, 60, 24, 22, 18, 49)
    pdf.set_font(FONT, '', 8)
    with pdf.table(col_widths=widths, line_height=4.5, text_align='LEFT',
                   headings_style=_heading_style()) as table:
        row = table.row()
        for header in headers:
            row.cell(str(header))
        for service in vehicle.service_set.order_by('-service_date'):
            row = table.row()
            row.cell(date_format(timezone.localtime(service.service_date),
                                 'SHORT_DATE_FORMAT'))
            row.cell(service.work_description or '')
            row.cell(service.remarks or '')
            row.cell('' if service.travel_distance is None
                     else str(service.travel_distance))
            row.cell('' if service.cost is None else str(service.cost))
            row.cell(_('Yes') if service.damage else '')
            row.cell(service.workshop or '')

    pdf.ln(3)
    _line(pdf, f'{_("Total cost")}: {vehicle.total_cost:.2f}', True)
    _line(pdf, f'{_("Total damage cost")}: {vehicle.total_damage_cost:.2f}',
          True)


def _heading_style():
    from fpdf.fonts import FontFace
    return FontFace(emphasis='BOLD', fill_color=(230, 230, 230))


def vehicles_pdf(vehicles: Iterable[Vehicle]) -> bytes:
    """Render one page (or more) per vehicle with its service history."""
    pdf = _new_pdf()
    for vehicle in vehicles:
        _add_vehicle(pdf, vehicle)
    return bytes(pdf.output())
