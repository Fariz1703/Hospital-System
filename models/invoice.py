# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalInvoice(models.Model):
    _name = 'hospital_system.invoice'
    _description = 'Hospital Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'invoice_id'
    _order = "id desc"

    invoice_id = fields.Char(
        string="Invoice Reference",
        readonly=True,
        copy=False,
        default="New",
        tracking=True
    )

    patient_id = fields.Many2one(
        'hospital_system.patient',
        string="Patient",
        required=True,
        tracking=True
    )

    doctor_id = fields.Many2one(
        'hospital_system.doctor',
        string="Doctor",
        required=True,
        tracking=True
    )



    assessment_id = fields.Many2one(
        'hospital_system.assessment',
        string="Assessment",
        tracking=True
    )

    invoice_date = fields.Date(
        string="Invoice Date",
        default=fields.Date.today,
        tracking=True
    )

    invoice_line_ids = fields.One2many(
        'hospital_system.invoice.line',
        'invoice_id',
        string="Invoice Lines"
    )

    total_amount = fields.Float(
        string="Total Amount",
        compute="_compute_total_amount",
        store=True,
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    active = fields.Boolean(default=True)

    @api.depends('invoice_line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.invoice_line_ids.mapped('subtotal'))


    @api.model
    def create(self, vals):
        if vals.get('invoice_id', 'New') == 'New':
            vals['invoice_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.invoice.sequence'
            ) or 'New'
        return super(HospitalInvoice, self).create(vals)


    def action_confirm(self):
        for rec in self:
            rec.state = 'open'

    def action_paid(self):
        for rec in self:
            rec.state = 'paid'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'