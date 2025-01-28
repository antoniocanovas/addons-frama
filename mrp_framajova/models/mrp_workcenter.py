from odoo import models, fields, api
import datetime


class MrpWorcenter(models.Model):
    _inherit = 'mrp.workcenter'

    update_lot_dates = fields.Boolean(
        string='update lot dates',
        help='Allow to update lot dates in production orders.'
    )



