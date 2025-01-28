from odoo import models, fields, api
import datetime


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'


    @api.constrains('state')
    def update_lot_dates(self):
        local_time = datetime.datetime.now()
        for record in self:
            # Verificamos todas las condiciones necesarias
            if (
                record.workcenter_id.update_lot_dates and
                record.finished_lot_id.id and
                record.product_id.use_expiration_date and
                record.state == 'done'
            ):
                # Calculamos las fechas basadas en los tiempos definidos
                expiration_date = local_time + datetime.timedelta(days=record.product_id.expiration_time)
                use_date = local_time + datetime.timedelta(days=record.product_id.use_time)
                removal_date = local_time + datetime.timedelta(days=record.product_id.removal_time)
                alert_date = local_time + datetime.timedelta(days=record.product_id.alert_time)

                # Actualizamos los campos del lote terminado
                record.finished_lot_id.write({
                    'expiration_date': expiration_date,
                    'use_date': use_date,
                    'removal_date': removal_date,
                    'alert_date': alert_date
                })
