from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    labels = fields.Integer(
        string="Labels",
        default=1,
        help="Indica cuántas etiquetas quieres que se impriman.",
    )
