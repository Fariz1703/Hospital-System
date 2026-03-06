# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hospital_system.doctor'
    _description = 'Doctor Master Data'
    _rec_name="doctor_name"
    _order = "id desc"

    doctor_name = fields.Char(
        string="Doctor Name",
        required=True
    )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')

    department_id= fields.Many2one(
        'hospital_system.department',string="Department",
        required=True
    )

    appendix= fields.Char(
        string="Doctor Appendix",
        required=True
        )
    
    doctor_id = fields.Char(
        string="Doctor Reference",
        readonly=True,
        copy=False,
        default="New"
    )

    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        if vals.get('doctor_id', 'New') == 'New':
            vals['doctor_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.doctor.sequence'
            ) or 'New'
        return super(Doctor, self).create(vals)