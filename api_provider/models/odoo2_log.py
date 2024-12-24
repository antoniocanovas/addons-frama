from odoo import models, fields


class Odoo2Log(models.Model):
    _name = "odoo2.log"
    _description = "Log de datos recibidos de Odoo1"

    name = fields.Text("Log")
    token_used = fields.Char("Token recibido")
    odoo1_config_id = fields.Many2one(
        "odoo2.odoo1.config",
        string="Config Odoo1",
        help="A qué configuración de Odoo1 corresponde esta petición.",
    )
