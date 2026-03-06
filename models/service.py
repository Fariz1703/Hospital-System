# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalService(models.Model):
    _name = 'hospital_system.service'
    _description = 'Hospital Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'service_name'
    _order = "id desc"

    service_id = fields.Char(
        string="Service Reference",
        readonly=True,
        copy=False,
        default="New"
    )

    service_name = fields.Char(
        string="Service Name",
        required=True,
        tracking=True
    )

    service_type = fields.Selection([
        ('consultation', 'Doctor Consultation'),
        ('procedure', 'Medical Procedure'),
        ('medicine', 'Medicine'),
        ('lab', 'Laboratory'),
        ('other', 'Other')
    ], string="Service Type", required=True, tracking=True)

    price = fields.Float(
        string="Price",
        tracking=True
    )

    description = fields.Text(
        string="Description",
        tracking=True
    )

    active = fields.Boolean(
        default=True
    )

    @api.model
    def create(self, vals):
        if vals.get('service_id', 'New') == 'New':
            vals['service_id'] = self.env['ir.sequence'].next_by_code(
                'hospital_system.service.sequence'
            ) or 'New'
        return super(HospitalService, self).create(vals)