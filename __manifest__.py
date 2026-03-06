# -*- coding: utf-8 -*-
{
    'name': "hospital_system",

'summary': "Hospital management system for patient registration, appointments, assessments, prescriptions, and payments",

'description': """
Hospital Management System module built for Odoo 17 to support basic healthcare service workflows.

This module allows hospital staff to manage patient operations efficiently, including:
- Patient registration and patient record management
- Appointment scheduling between patients and doctors
- Patient check-in and queue management
- Doctor assessment with detailed medical information
- Prescription creation for patients
- Payment processing after consultation

The system is developed using custom Odoo models, views, and workflows to simulate a simple hospital operational system.
""",

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'demo/sequence_demo.xml',
        'views/service.xml',
        'views/invoice.xml',
        'views/assesment.xml',
        'views/appointment.xml',
        'views/patient_registration.xml',
        'views/department.xml',
        'views/doctor.xml',
        'views/patient.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/department_demo.xml',
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/service_demo.xml',
    ],
}

