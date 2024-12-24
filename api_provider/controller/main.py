import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class Odoo2Controller(http.Controller):

    @http.route(
        "/odoo2/receive_data", type="json", auth="public", methods=["POST"], csrf=False
    )
    def receive_data(self):
        """
        Endpoint para recibir datos desde Odoo 1.
        """
        # Obtenemos los datos que llegan en formato JSON
        data = json.loads(request.httprequest.data.decode("utf-8"))
        question = data.get("question")
        token = data.get("token")
        config_token = data.get(
            "config_token"
        )  # si Odoo1 manda un 'config_token' diferente

        # Validar que venga la pregunta
        if not question:
            return {"error": "No se recibió la pregunta"}

        # Localizar la configuración en Odoo 2, si la manejas mediante un token.
        # Supongamos que en Odoo 2 guardas distintos tokens en el modelo `odoo2.odoo1.config`.
        config_obj = (
            request.env["odoo2.odoo1.config"]
            .sudo()
            .search([("token_odoo1", "=", config_token)], limit=1)
        )

        if not config_obj:
            # También podrías simplemente chequear si token == 'TOKEN_VALIDO' en lugar de un search en la DB
            return {"error": "Token inválido o config no encontrada"}

        # Guardar en el log de Odoo 2
        created_log = (
            request.env["odoo2.log"]
            .sudo()
            .create(
                {
                    "name": f"Pregunta recibida: {question}",
                    "token_used": token or "",
                    "odoo1_config_id": config_obj.id,
                }
            )
        )

        _logger.info("Registro creado en odoo2.log con ID %s", created_log.id)

        # (Opcional) Llamada de vuelta a Odoo 1
        # --------------------------------------
        # Si quieres hacer una llamada a Odoo 1 (ejemplo, un JSON-RPC),
        # y tienes almacenados datos en config_obj (url_odoo1, credenciales, etc.), podrías hacerlo aquí.
        #
        # Ejemplo muy simplificado de JSON-RPC:
        #
        # import requests
        # url_odoo1 = config_obj.url_odoo1  # asumiendo que guardas una URL de Odoo 1
        # json_data = {
        #     "jsonrpc": "2.0",
        #     "method": "call",
        #     "params": {
        #         "service": "object",
        #         "method": "execute_kw",
        #         "args": [
        #             "db_odoo1",
        #             2,  # admin user ID
        #             "admin_password_odoo1",
        #             "odoo1.question",
        #             "write",
        #             [[record_id]],  # IDs de los registros a actualizar
        #             {"info_raw": f"Pregunta recibida: {question} desde Odoo 2"},
        #         ]
        #     },
        #     "id": 1
        # }
        # try:
        #     rpc_response = requests.post(url_odoo1, json=json_data, timeout=10)
        # except Exception as e:
        #     _logger.error("Error RPC con Odoo1: %s", e)
        #

        # Respondemos a Odoo 1
        return {
            "status": "OK",
            "log_id": created_log.id,
            "message": f"Recibida y guardada la pregunta: {question}",
        }
