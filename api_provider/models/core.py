from odoo import http
from odoo.http import request


class ContactsAPI(http.Controller):

    @http.route('/api/contacts', type='json', auth='none', methods=['POST'], csrf=False)
    def get_contacts(self, **kwargs):
        # Extrae el token del cuerpo de la solicitud
        token = kwargs.get('token')

        if not token:
            return {
                'error': 'Missing token',
                'code': 400
            }

        # Verifica el token
        valid_token = "123456789"
        if token != valid_token:
            return {
                'error': 'Invalid token',
                'code': 403
            }

        # Obtén los contactos
        contacts = request.env['res.partner'].sudo().search([])
        contact_data = [{
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
        } for contact in contacts]

        return {
            'contacts': contact_data
        }

