# -*- coding: utf-8 -*-
from odoo import api, models

class Contract(models.Model):
    _inherit = "hr.contract"
    
    @api.model
    def create(self,vals):
        res = super(Contract,self).create(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def write(self,vals):
        res = super(Contract,self).write(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def unlink(self):
        res = super(Contract,self).unlink()
        self.env['ir.rule'].clear_caches()
        return res
