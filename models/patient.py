# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class Patient(models.Model):
    _name = 'hospital_system.patient'
    _description = 'Patient'
    _rec_name = 'patient_name'
    _inherit=["mail.thread",
            "mail.activity.mixin"]
    _order = "id desc"

    patient_name = fields.Char(string='Patient Name', required=True, tracking=True)
    patient_id = fields.Char(string='Patient ID', readonly=True, copy=False, default='New', tracking=True)
    identity_number = fields.Char(
        string='Identity Number',
        tracking=True
    )

    _sql_constraints = [
        (
            'unique_identity_number',
            'unique(identity_number)',
            'Identity Number must be unique!'
        )
    ]

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', tracking=True)

    birth_date = fields.Date(string='Birth Date', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)

    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address', tracking=True)

    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string='Blood Type', tracking=True)

    active = fields.Boolean(default=True, tracking=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if vals.get('patient_id', 'New') == 'New':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.patient.sequence'
            ) or 'New'
        return super(Patient, self).create(vals)
    
    def action_make_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'res_model': 'hospital_system.appointment',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
            }
        }
    