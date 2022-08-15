# -*- coding: utf-8 -*-
from odoo import api, models

class Department(models.Model):
    _inherit = "hr.department"
    
    @api.model
    def create(self,vals):
        res = super(Department,self).create(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def write(self,vals):
        res = super(Department,self).write(vals)
        self.env['ir.rule'].clear_caches()
        return res

    def unlink(self):
        res = super(Department,self).unlink()
        self.env['ir.rule'].clear_caches()
        return res

    def get_departments_childs(self):
        result = self.env['hr.department']
        for obj in self:
            result += obj
            if obj.child_ids:
                result += obj.child_ids.get_departments_childs()
        return result
