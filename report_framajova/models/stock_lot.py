from odoo import fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    mrp_production_id = fields.Many2one(
        'mrp.production',  # Add this line to specify the comodel
        string='mrp production',
        compute="_compute_mrp_production_id",
    )

    def _compute_mrp_production_id(self):
        for record in self:
            production = self.env['mrp.production'].search_read([('lot_producing_id', '=', record.id)], ['id'], limit=1)
            record['mrp_production_id'] = production[0]['id'] if production else False
