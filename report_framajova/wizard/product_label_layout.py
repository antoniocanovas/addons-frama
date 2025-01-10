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
        # Llamar al método original
        xml_id, data = super()._prepare_report_data()

        # Personalizar para 101x151
        if self.print_format == "101x151":
            xml_id = "report_framajova.stock_warehouse_label_report"
            if not data.get("active_ids"):
                data["active_ids"] = self.env.context.get("active_ids", [])
            # Asegurarse de pasar docids correctamente
            if not data["active_ids"]:
                raise ValueError("No active_ids found in context or data!")

        print(f"Prepared Data: {data}")
        return xml_id, data

