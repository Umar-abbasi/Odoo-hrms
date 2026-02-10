{
    'name': 'University Employee Management',
    'version': '19.0.1.0.0',
    'summary': 'University HR System (Linked to Odoo)',
    'category': 'Human Resources',
    'author': 'Umar',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/change_status_views.xml',
        'views/employee_views.xml',
        'views/job_views.xml',
        'views/config_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}