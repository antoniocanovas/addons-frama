from odoo import models, fields, api
import datetime


class MrpWorcenter(models.Model):
    _inherit = 'mrp.workcenter'

    next_workcenter_ids = fields.Many2many(
        'mrp.workcenter',
        'mrp_next_workcenter_rel',
        'workcenter_id',
        'next_workcenter_id',
        domain="['|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        string="Next Workcenters", check_company=True,
        help="Alternative workcenters that can be substituted to this one in order to dispatch production"
    )

    next_workcenter_id = fields.Many2one(
        'mrp.workcenter',
        string="Default next",
        help="Default workcenter assigned to the next operation",
    )