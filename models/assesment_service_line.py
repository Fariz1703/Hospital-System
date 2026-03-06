# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AssessmentServiceLine(models.Model):
    _name = 'hospital_system.assessment.service.line'
    _description = 'Assessment Service Line'
    _order = "id desc"

    assessment_id = fields.Many2one(
        'hospital_system.assessment',
        string="Assessment",
        required=True,
        ondelete='cascade'
    )

    service_id = fields.Many2one(
        'hospital_system.service',
        string="Service",
        required=True
    )

    quantity = fields.Integer(default=1)

    price = fields.Float(
        related='service_id.price',
        store=True
    )

    subtotal = fields.Float(
        compute='_compute_subtotal',
        store=True
    )

    @api.depends('quantity', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price