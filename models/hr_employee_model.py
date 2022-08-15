# -*- coding: utf-8 -*-
from odoo import api,fields, models

class Employee(models.Model):
    _inherit = "hr.employee"

    av_contracts_count = fields.Integer(
        compute='_compute_av_contracts_count',
        string='Available Contract Count')

    vehicle = fields.Char(string='Company Vehicle', groups="hr.group_hr_user,department_contracts_access.group_hr_contract_department_manager")
    contract_warning = fields.Boolean(string='Contract Warning', store=True, compute='_compute_contract_warning', groups="hr.group_hr_user,department_contracts_access.group_hr_contract_department_manager")
    first_contract_date = fields.Date(compute='_compute_first_contract_date', groups="hr.group_hr_user,department_contracts_access.group_hr_contract_department_manager")
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user,department_contracts_access.group_hr_contract_department_manager", copy=False)

    def _compute_av_contracts_count(self):
        for obj in self:
            obj.av_contracts_count = len(obj.contract_ids) or 0

    @api.onchange('contract_ids')
    def onchange_contract_ids(self):
        for obj in self:
            self.env['ir.rule'].clear_caches()
