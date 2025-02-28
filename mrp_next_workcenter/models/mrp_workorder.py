from odoo import models, fields, api
import datetime




class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    next_workcenter_ids = fields.Many2many(
        related='workcenter_id.next_workcenter_ids',)



    def process_next_workcenter(self,next_workcenter_id):
        for record in self:
            operation_id = record.operation_id
            next_workorder_id = self.env['mrp.workorder'].search([
                ('operation_id.sequence', '=', operation_id.sequence+1),
                ('production_id', '=', record.production_id.id),
            ])
            if next_workorder_id:
                next_workorder_id.write({'workcenter_id': next_workcenter_id})

    @api.constrains('state')
    def process_default_next_workcenter(self):
        for record in self:
            if record.state == 'ready':
                operation_id = record.operation_id
                next_workorder_id = self.env['mrp.workorder'].search([
                    ('operation_id.sequence', '=', operation_id.sequence+1),
                    ('production_id', '=', record.production_id.id),
                ])
                if next_workorder_id:
                    next_workorder_id.write({'workcenter_id': record.workcenter_id.next_workcenter_id.id})





    def get_next_worcenter_ids(self):
        self.ensure_one()
        # Devuelve una lista de tuplas (id, name) para cada workcenter
        return [(wc.id, wc.display_name) for wc in self.next_workcenter_ids]


