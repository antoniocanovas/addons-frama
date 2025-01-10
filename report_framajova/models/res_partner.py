from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_without_price = fields.Boolean(
        string='Purchase Without Price',
        help='Allow purchases without a defined price.'
    )
