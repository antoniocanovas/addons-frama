from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sale_id = fields.Many2one(related='picking_id.sale_id', )
    partner_id = fields.Many2one(related='sale_id.partner_id', )
