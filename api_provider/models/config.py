from odoo import models, fields


class Odoo1ConnectionConfig(models.Model):
    """
    Modelo para almacenar la configuración de las distintas
    instancias Odoo 1 que se conectan a Odoo 2.
    """

    _name = "odoo2.odoo1.config"
    _description = "Configuración de múltiples Odoo 1"

    name = fields.Char(string="Nombre", required=True)
    token_odoo1 = fields.Char(
        string="Token de Odoo1",
        required=True,
        help="Token con el que Odoo1 se identifica al llamar a Odoo2.",
    )

    # Si quieres hacer llamadas de vuelta a Odoo1, podrías guardar esto:
    # url_odoo1 = fields.Char(string="URL Odoo1",
    #                         help="Ejemplo: https://mi-odoo1.com/jsonrpc")
    # database_odoo1 = fields.Char(string="BD Odoo1")
    # user_odoo1 = fields.Char(string="Usuario Odoo1")
    # password_odoo1 = fields.Char(string="Password Odoo1", groups="base.group_system")
