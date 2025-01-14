from odoo import models, fields, api
import json
from collections import defaultdict

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    sml_ids = fields.Text(
        string="Grouped Stock Move Lines",
        compute="_compute_sml_ids",
        store=False
    )

    @api.depends('line_ids')
    def _compute_sml_ids(self):
        for record in self:
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
                            'expiration_date': sml.lot_id.expiration_date.strftime('%d/%m/%Y') if sml.lot_id.expiration_date else '',
                        })
            # Ordenar las claves del diccionario alfabéticamente
            sorted_grouped_data = dict(sorted(grouped_data.items()))
            record.sml_ids = json.dumps(sorted_grouped_data)
