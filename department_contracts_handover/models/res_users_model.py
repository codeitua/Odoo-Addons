# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    contract_rule_ids = fields.One2many('contract.handover.rule','access_receiver_id',string='Assigned contract rules')

    def get_contract_ids(self):
        """This method called by rules"""
        for obj in self:
            if self.env.user.has_group('hr_contract.group_hr_contract_manager'):
                return self.env['hr.contract'].sudo().search([]).ids
            return obj.contract_rule_ids.get_contracts()
