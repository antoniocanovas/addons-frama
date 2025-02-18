from odoo import models

class StockInvoiceOnshippingInherit(models.TransientModel):
    _inherit = "stock.invoice.onshipping"

    def _get_invoice_line_values(self, moves, invoice_values, invoice):
        # Llamamos al método original para obtener los valores base
        values = super(StockInvoiceOnshippingInherit, self)._get_invoice_line_values(moves, invoice_values, invoice)
        # Añadimos la clave "sale_line_ids" con la lista de ids correspondientes
        values.update({
            "sale_line_ids": [(6, 0, moves.mapped("sale_line_id").ids)]
        })
        return values
