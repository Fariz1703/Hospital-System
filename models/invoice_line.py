# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HospitalInvoiceLine(models.Model):
    _name = 'hospital_system.invoice.line'
    _description = 'Hospital Invoice Line'
    _order = "id desc"

    invoice_id = fields.Many2one(
        'hospital_system.invoice',
        string="Invoice",
        required=True,
        ondelete="cascade"
    )

    service_id = fields.Many2one(
        'hospital_system.service',
        string="Service",
        required=True
    )

    quantity = fields.Integer(
        default=1
    )

    price = fields.Float(
        string="Price"
    )

    subtotal = fields.Float(
        compute="_compute_subtotal",
        store=True
    )

    @api.depends('quantity', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price