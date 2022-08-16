# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    contract_rule_ids = fields.One2many('contract.handover.rule','access_receiver_id',string='Assigned contract rules')

    def get_manager_empl(self):
        for obj in self:
            res = []
            if not obj.employee_id:
                return False
            department_ids = self.env['hr.department'].search([('manager_id','=',obj.employee_id.id)])
            if department_ids:
                employees = department_ids.get_departments_childs().mapped('member_ids')
                res = employees.filtered(lambda empl: empl.id != obj.employee_id.id).ids
            return res

    def get_manager_contract(self):
        for obj in self:
            empl_list = obj.get_manager_empl()
            contracts = self.env['hr.contract'].sudo().search([
                        ('employee_id','in',empl_list)])
            if contracts:
                return contracts.ids

    def get_contract_ids(self):
        """This method called by rules"""
        for obj in self:
            if self.env.user.has_group('hr_contract.group_hr_contract_manager'):
                return self.env['hr.contract'].sudo().search([]).ids
            
            result = obj.sudo().contract_rule_ids.get_contracts()
            if obj.employee_ids:
                manager_contracts = obj.get_manager_contract()
                if manager_contracts:
                    result += manager_contracts
            return result

    def get_employee_ids(self):
        """This method called by rules"""
        for obj in self:
            if self.env.user.has_group('hr_contract.group_hr_contract_manager') or not self.env.user.has_group('department_contracts_access.group_hr_contract_department_manager'):
                return self.env['hr.employee'].sudo().search([]).ids

            result = obj.sudo().contract_rule_ids.get_employees()
            if obj.employee_ids:
                result += obj.get_manager_empl()
            return result
