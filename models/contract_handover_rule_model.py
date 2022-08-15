# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date

import time

class ContractHandoverRule(models.Model):
    _name = "contract.handover.rule"
    _description = "Contract handover rule"
    _order = "id desc"

    department_id = fields.Many2one('hr.department', string='Department', required=True, ondelete='cascade')
    access_provider_id = fields.Many2one('res.users', string='Access provider', required=True, default=lambda self: self.env.user)
    access_receiver_id = fields.Many2one('res.users', string='Access receiver', required=True, ondelete='cascade',domain=lambda self: [('employee_ids','!=',False),("groups_id", "=", self.env.ref( "department_contracts_access.group_hr_contract_department_manager").id)])
    expiration_date = fields.Date(string='Expiration date')
    date_message = fields.Text(string='Date warning', default='If the expiration date is not set, infinite access will be provided.')
    share_to_manager = fields.Boolean(string="Share Department Manager's Contract", default=False)

    @api.model
    def create(self,vals):
        res = super(ContractHandoverRule,self).create(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def write(self,vals):
        res = super(ContractHandoverRule,self).write(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def unlink(self):
        res = super(ContractHandoverRule,self).unlink()
        self.env['ir.rule'].clear_caches()
        return res

    def get_contracts(self):
        """returns list of ids"""
        result = []
        empl_ids = self.get_employees()
        contracts_ids = self.env['hr.contract'].sudo().search([('employee_id','in',empl_ids)])
        if contracts_ids:
            result += contracts_ids.ids
        return result

    def get_employees(self):
        result = []
        for obj in self:
            if not obj.expiration_date or obj.expiration_date >= date.today():
                department_ids = obj.department_id.get_departments_childs()
                employee_ids = department_ids.mapped('member_ids')
                if not obj.share_to_manager and obj.department_id.manager_id:
                    employee_ids = employee_ids.filtered(lambda empl: empl.id != obj.department_id.manager_id.id)
                if employee_ids:
                    result += employee_ids.ids
        return result

    @api.depends('department_id', 'access_receiver_id','expiration_date')
    def name_get(self):
        res = []
        for obj in self:
            name = f"{obj.access_receiver_id.name} ({obj.department_id.name})"
            res.append((obj.id, name))
        return res

    def delete_expired_rules(self):
        """CRON method which deletes all expired rules"""
        rules_ids = self.env['contract.handover.rule'].sudo().search([])
        rules_to_delete = rules_ids.filtered(lambda rule: rule.expiration_date and rule.expiration_date < date.today())
        if rules_to_delete:
            rules_to_delete.unlink()

    @api.constrains('expiration_date')
    def _validate_expiration_date(self):
        for record in self:
            if record.expiration_date and record.expiration_date < date.today():
                raise ValidationError("Please select a later date.")
