# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class SignSendRequest(models.TransientModel):
    _inherit = "sign.send.request"

    task_id = fields.Many2one("project.task", string="Task")

    def create_request(self):
        # Call the original create_request method
        sign_request = super(SignSendRequest, self).create_request()
        # Assign the task_id to the created sign_request
        sign_request.task_id = self.task_id
        return sign_request
