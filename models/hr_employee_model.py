# -*- coding: utf-8 -*-
from odoo import api,fields, models

class Employee(models.Model):
    _inherit = "hr.employee"

    av_contracts_count = fields.Integer(
        compute='_compute_av_contracts_count',
        string='Available Contract Count')

    def _compute_av_contracts_count(self):
        for obj in self:
            obj.av_contracts_count = len(obj.contract_ids) or 0

    @api.onchange('contract_ids')
    def onchange_contract_ids(self):
        for obj in self:
            self.env['ir.rule'].clear_caches()