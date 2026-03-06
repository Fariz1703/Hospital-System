# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DoctorAssessment(models.Model):
    _name = 'hospital_system.assessment'
    _description = 'Doctor Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'assessment_id'
    _order = "id desc"

    assessment_id = fields.Char(
        string="Assessment Reference",
        readonly=True,
        copy=False,
        default="New",
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


    appointment_id = fields.Many2one(
        'hospital_system.appointment',
        string="Appointment",
        required=True,
        tracking=True,
        ondelete="cascade",
        readonly='1'
    )

    patient_id = fields.Many2one(
        'hospital_system.patient',
        string="Patient",
        related="appointment_id.patient_id",
        store=True,
        readonly=True,
        tracking=True
    )

    doctor_id = fields.Many2one(
        'hospital_system.doctor',
        string="Doctor",
        related="appointment_id.doctor_id",
        store=True,
        readonly=True,
        tracking=True
    )

    assessment_date = fields.Datetime(
        string="Assessment Date",
        default=fields.Datetime.now,
        tracking=True
    )

    service_line_ids = fields.One2many(
        'hospital_system.assessment.service.line',
        'assessment_id',
        string="Services"
    )

    temperature = fields.Float(
        string="Temperature (°C)",
        tracking=True
    )

    blood_pressure = fields.Char(
        string="Blood Pressure",
        tracking=True
    )

    heart_rate = fields.Integer(
        string="Heart Rate",
        tracking=True
    )

    respiratory_rate = fields.Integer(
        string="Respiratory Rate",
        tracking=True
    )

    weight = fields.Float(
        string="Weight (kg)",
        tracking=True
    )

    height = fields.Float(
        string="Height (cm)",
        tracking=True
    )


    chief_complaint = fields.Text(
        string="Chief Complaint",
        tracking=True
    )

    diagnosis = fields.Text(
        string="Diagnosis",
        tracking=True
    )

    treatment_plan = fields.Text(
        string="Treatment Plan",
        tracking=True
    )

    notes = fields.Text(
        string="Doctor Notes",
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('assessment_id', 'New') == 'New':
            vals['assessment_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.assessment.sequence'
            ) or 'New'
        return super().create(vals)

    def action_start(self):

        for rec in self:

            today = fields.Date.today()

            previous_queue = self.search([
                ('doctor_appendix', '=', rec.doctor_appendix),
                ('queue_number', '<', rec.queue_number),
                ('state', '!=', 'done'),
                ('assessment_date', '>=', today),
            ], limit=1)

            if previous_queue:
                raise ValidationError(
                    "There is still a previous queue that has not been completed."
                )

            rec.appointment_id.action_start_consultation()
            rec.state = 'in_progress'

    def action_done(self):

        for rec in self:

            invoice_lines = []

            for line in rec.service_line_ids:
                invoice_lines.append((0, 0, {
                    'service_id': line.service_id.id,
                    'quantity': line.quantity,
                    'price': line.price,
                }))

            invoice = self.env['hospital_system.invoice'].create({
                'state': 'open',
                'patient_id': rec.patient_id.id,
                'doctor_id': rec.doctor_id.id,
                'assessment_id': rec.id,
                'invoice_line_ids': invoice_lines
            })

            rec.appointment_id.action_done()
            rec.state = 'done'

    def action_cancel(self):
        self.appointment_id.action_cancel()
        self.state = 'cancel'