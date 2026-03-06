# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Department(models.Model):
    _name = 'hospital_system.department'
    _description = 'Department Master Data'
    _rec_name="department_name"
    _order = "id desc"


    department_id = fields.Char(
        string="Department Reference",
        readonly=True,
        copy=False,
        default="New"
    )

    department_name = fields.Char(
        string="Department Name", 
        required=True
        )
    
    department_type = fields.Selection([
            ('management', 'Management'),
            ('medical', 'Medical')
        ], 
        string="Department Type",
        required=True)
    
    @api.model
    def create(self, vals):
        if vals.get('department_id', 'New') == 'New':
            vals['department_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.department.sequence'
            ) or 'New'
        return super(Department, self).create(vals)

