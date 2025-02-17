from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_label_data(self):
        """Construye una lista de diccionarios con la información de cada etiqueta,
        usando las líneas de movimiento (move_lines y move_line_ids) y la cantidad ejecutada (qty_done).
        """
        label_data = []
        for move in self.move_lines:
            for line in move.move_line_ids:
                if int(move.product_packaging_quantity):
                    packaging_qty = move.product_packaging_quantity
                    # Usamos qty_done de la línea como cantidad real procesada
                    if line.qty_done % packaging_qty == 0:
                        labels_count = int(line.qty_done / packaging_qty)
                    else:
                        labels_count = int(line.qty_done / packaging_qty) + 1
                    for i in range(labels_count):
                        qty = packaging_qty if i < labels_count - 1 else line.qty_done - packaging_qty * (labels_count - 1)
                        label_data.append({
                            'counter': i + 1,
                            'total': labels_count,
                            'current_qty': qty,
                            'line': line,
                        })
                else:
                    # Sin packaging definido, una única etiqueta
                    label_data.append({
                        'counter': 1,
                        'total': 1,
                        'current_qty': line.qty_done,
                        'line': line,
                    })
        return label_data

    @api.model
    def get_report_values(self, docids, data=None):
        pickings = self.browse(docids)
        # Creamos un diccionario que asocia cada picking.id a su lista de etiquetas
        label_data = {}
        for picking in pickings:
            label_data[picking.id] = picking._get_label_data()
        return {
            'docs': pickings,
            'label_data': label_data,
        }
