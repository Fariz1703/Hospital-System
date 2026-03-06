# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Appointment(models.Model):
    _name = 'hospital_system.appointment'
    _description = 'Appointment'
    _rec_name = 'appointment_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    appointment_id = fields.Char(
        string="Appointment Reference",
        readonly=True,
        copy=False,
        default="New",
        tracking=True
    )

    patient_id = fields.Many2one(
        'hospital_system.patient',
        string="Patient",
        required=True,
        tracking=True,
        readonly=True
    )

    appointment_date = fields.Date(
        string="Appointment Date", 
        required=True,
        tracking=True
    )

    department_id = fields.Many2one(
        'hospital_system.department',
        string="Department",
        required=True,
        domain=[('department_type', '=', 'medical')],
        tracking=True
    )

    doctor_id = fields.Many2one(
        'hospital_system.doctor',
        string="Doctor",
        required=True,
        tracking=True
    )

    chief_complaint = fields.Text(
        string="Chief Complaint",
        tracking=True
    )

    doctor_appendix = fields.Char(
        string="Doctor Appendix",
        readonly=True
    )

    
    queue_number = fields.Integer(
        string="Queue Number",
        readonly=True
    )

    appendix_number = fields.Char(
        string="Queue",
        readonly=True
    )

    checkin_time = fields.Datetime(
        string="Check In Time",
        readonly=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Appointment Confirmed'),
        ('checkin', 'Check In'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        if vals.get('appointment_id', 'New') == 'New':
            vals['appointment_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.appointment.sequence'
            ) or 'New'
        return super().create(vals)

    @api.onchange('department_id')
    def _onchange_department(self):
        self.doctor_id = False
        self.doctor_appendix = False


    def action_confirm(self):
        for rec in self:
            rec.doctor_appendix = self.doctor_id.appendix
            rec.state = 'confirmed'

    def action_checkin(self):

        for rec in self:

            if rec.appointment_date != fields.Date.today():
                raise ValidationError(
                    "Check-in is only allowed on the appointment date."
                )

            now = fields.Datetime.now()

            last_queue = self.search([
                ('doctor_id', '=', rec.doctor_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('state', 'in', ['checkin', 'in_consultation', 'done'])
            ], order='queue_number desc', limit=1)

            next_queue = 1

            if last_queue:
                next_queue = last_queue.queue_number + 1

            rec.queue_number = next_queue

            if rec.doctor_appendix:
                rec.appendix_number = f"{rec.doctor_appendix}-{next_queue}"
            else:
                rec.appendix_number = str(next_queue)

            rec.checkin_time = now
            rec.state = 'checkin'
            self.env['hospital_system.assessment'].create({
                'doctor_id': rec.doctor_id.id,
                'patient_id': rec.patient_id.id,
                'doctor_appendix': rec.doctor_appendix,
                'queue_number': rec.queue_number,
                'appendix_number': rec.appendix_number,
                'appointment_id': rec.id,
            })


    def action_start_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'