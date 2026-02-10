from odoo import models, fields

class Department(models.Model):
    _inherit = 'hr.department'

    code = fields.Char(string="Department Code", index=True)

    _sql_constraints = [
        ('unique_dept_code', 'unique(code)', 'Department Code must be unique!')
    ]