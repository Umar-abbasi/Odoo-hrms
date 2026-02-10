from odoo import models, fields, api

class EmployeeStatusWizard(models.TransientModel):
    _name = 'employee.status.wizard'
    _description = 'Change Employee Status'

    new_state = fields.Selection([
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
        ('compulsory_retired', 'Compulsory Retired'),
        ('terminated', 'Terminated'),
        ('removed', 'Removal from Service'),
        ('dismissed', 'Dismissal from Service'),
        ('deceased', 'Deceased'),
        ('archived', 'Archived')
    ], string="New Status", required=True)

    def action_confirm_status(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            employee = self.env['hr.employee'].browse(active_id)
            employee.write({'state': self.new_state})