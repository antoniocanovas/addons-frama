from odoo import models, fields, api
import json
from collections import defaultdict


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    sml_ids = fields.Text(
        string="Grouped Stock Moves",
        compute="_compute_sml_ids",
        store=False
    )

    sml_m2m_ids = fields.Many2many(
        comodel_name='stock.move',
        string="Albaranes para imprimir",
        help="Selecciona los movimientos de stock relacionados con esta factura."
    )

    sml_m2m_domain_ids = fields.Many2many(
        comodel_name='stock.move',
        compute="_compute_sml_m2m_domain",
        store=False
    )

    @api.depends('invoice_line_ids')
    def _compute_sml_m2m_domain(self):
        """
        Calcula los movimientos de stock relacionados con las líneas de factura
        y los almacena en `sml_m2m_domain_ids` para usar en el domain.
        """
        for record in self:
            grouped_moves = self.env['stock.move']
            for line in record.invoice_line_ids:
                for move in line.move_line_ids:
                    grouped_moves |= move  # Agregamos los movimientos

            record.sml_m2m_domain_ids = grouped_moves

    @api.depends('sml_m2m_ids')
    def _compute_sml_ids(self):
        for record in self:
            if  record.sml_m2m_ids:

                grouped_data = defaultdict(list)

                for move in record.sml_m2m_ids:
                    for sml in move.move_line_ids:
                        grouped_data[sml.reference].append({
                            'product_name': sml.product_id.display_name,
                            'quantity': sml.qty_done,
                            'uom_name': sml.product_uom_id.name,
                            'lot_name': sml.lot_id.name,
                            'date': sml.date.strftime('%d/%m/%Y') if sml.date else '',
                            'expiration_date': sml.lot_id.expiration_date.strftime(
                                '%d/%m/%Y') if sml.lot_id.expiration_date else '',
                        })
                # Ordenar las claves del diccionario alfabéticamente
                sorted_grouped_data = dict(sorted(grouped_data.items()))
                record.sml_ids = json.dumps(sorted_grouped_data)
            else:
                grouped_data = defaultdict(list)
                for line in record.invoice_line_ids:
                    for move in line.move_line_ids:
                        for sml in move.move_line_ids:
                            grouped_data[sml.reference].append({
                                'product_name': sml.product_id.display_name,
                                'quantity': sml.qty_done,
                                'uom_name': sml.product_uom_id.name,
                                'lot_name': sml.lot_id.name,
                                'date': sml.date.strftime('%d/%m/%Y') if sml.date else '',
                                'expiration_date': sml.lot_id.expiration_date.strftime(
                                    '%d/%m/%Y') if sml.lot_id.expiration_date else '',
                            })
                # Ordenar las claves del diccionario alfabéticamente
                sorted_grouped_data = dict(sorted(grouped_data.items()))
                record.sml_ids = json.dumps(sorted_grouped_data)


@api.onchange('invoice_line_ids')
def _onchange_fill_sml_m2m_ids(self):
    """
    Cuando cambian las líneas de la factura, sugiere movimientos de stock
    basados en las líneas de factura.
    """
    for record in self:
        if not record.sml_m2m_ids:  # Solo si el usuario no ha seleccionado manualmente
            record.sml_m2m_ids = record.sml_m2m_domain_ids
