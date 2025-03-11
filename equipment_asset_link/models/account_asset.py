# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    equipment_ids = fields.One2many(
        'maintenance.equipment',
        'account_asset_id',
        string='Related Equipment',
        help='Equipment associated with this accounting asset'
    )
    equipment_count = fields.Integer(
        compute='_compute_equipment_count',
        string='Equipment Count',
        store=True  # Make it stored to enable search
    )
    has_equipment = fields.Boolean(
        string='Has Equipment',
        compute='_compute_equipment_count',
        store=True  # Make it stored to enable search
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for asset in self:
            count = len(asset.equipment_ids)
            asset.equipment_count = count
            asset.has_equipment = count > 0

    def action_view_equipments(self):
        self.ensure_one()
        return {
            'name': _('Related Equipment'),
            'view_mode': 'tree,form',
            'res_model': 'maintenance.equipment',
            'domain': [('account_asset_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_account_asset_id': self.id}
        }

    def unlink(self):
        for asset in self:
            if asset.equipment_ids:
                raise ValidationError(_(
                    'You cannot delete this accounting asset because it has linked equipment. '
                    'Please remove the reference in the associated equipment first.'
                ))
        return super(AccountAsset, self).unlink()