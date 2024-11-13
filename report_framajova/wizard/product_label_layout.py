# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductLabelLayoutInherited(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("101x151", "101 x 151 Custom Format")],
        default="101x151",
        ondelete={"101x151": "set default"},
    )

    def _prepare_report_data(self):
        # Llamada al método original para obtener xml_id y data iniciales
        xml_id, data = super()._prepare_report_data()

        # Modificar xml_id si el formato es 101x151
        if self.print_format == "101x151":

            xml_id = "report_framajova.report_action_product_template_label_101x151"

        return xml_id, data
