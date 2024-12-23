# controllers/contacts_api.py
from odoo import http
from odoo.http import request


class ContactsAPI(http.Controller):
    @http.route("/api/contacts", type="json", auth="none", methods=["POST"], csrf=False)
    def get_contacts(self, token, **kwargs):
        # Verifica el token
        valid_token = "123456789"
        if token != valid_token:
            return {"error": "Invalid token"}

        # Obtén los contactos
        contacts = request.env["res.partner"].sudo().search([])
        contact_data = [
            {
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
            }
            for contact in contacts
        ]

        return {"contacts": contact_data}
