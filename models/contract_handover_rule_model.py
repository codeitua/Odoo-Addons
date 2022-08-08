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
    access_receiver_id = fields.Many2one('res.users', string='Access receiver', required=True, ondelete='cascade')
    expiration_date = fields.Date(string='Expiration date')
    date_message = fields.Text(string='Date warning', default='If the expiration date is not set, infinite access will be provided.')
    share_to_manager = fields.Boolean(string="Share the Department Manager's Contract", default=False)

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
        for obj in self:
            if not obj.expiration_date or obj.expiration_date >= date.today():
                department_ids_list = (obj.department_id + obj.department_id.child_ids).ids
                if not obj.share_to_manager and obj.department_id.manager_id:
                    contract_ids = self.env['hr.contract'].sudo().search([
                        ('department_id','in',department_ids_list),
                        ('employee_id','!=',obj.department_id.manager_id.id)])
                    if contract_ids:
                        result+=contract_ids.ids
                else:
                    contract_ids = self.env['hr.contract'].sudo().search(['|',
                        ('department_id','in',department_ids_list),('employee_id','=',obj.department_id.manager_id.id)])
                    if contract_ids:
                        result+=contract_ids.ids
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
        # rules_ids = self.env['contract.handover.rule'].sudo().search([('expiration_date','<',date.today())])
        rules_ids = self.env['contract.handover.rule'].sudo().search([])
        rules_to_delete = rules_ids.filtered(lambda rule: rule.expiration_date and rule.expiration_date < date.today())
        if rules_to_delete:
            rules_to_delete.unlink()

    @api.constrains('expiration_date')
    def _validate_expiration_date(self):
        for record in self:
            if record.expiration_date and record.expiration_date < date.today():
                raise ValidationError("Please select a later date.")
