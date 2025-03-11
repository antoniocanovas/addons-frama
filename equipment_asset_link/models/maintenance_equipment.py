from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    account_asset_id = fields.Many2one(
        'account.asset',
        string='Accounting Asset',
        groups='account.group_account_user',
        help='Accounting asset associated with this equipment'
    )