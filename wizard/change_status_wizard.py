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

    # --- NEW FIELDS FOR UPLOAD ---
    office_order = fields.Binary(string="Office Order / Letter", required=True)
    file_name = fields.Char(string="File Name")

    def action_confirm_status(self):
        # Get the active employee
        active_id = self.env.context.get('active_id')
        if active_id:
            employee = self.env['hr.employee'].browse(active_id)
            
            # 1. Capture Old Status (Format nicely)
            old_state_label = dict(employee._fields['state'].selection).get(employee.state, employee.state)
            new_state_label = dict(self._fields['new_state'].selection).get(self.new_state, self.new_state)

            # 2. Create History Record
            self.env['employee.status.history'].create({
                'employee_id': employee.id,
                'date': fields.Datetime.now(),
                'user_id': self.env.uid,
                'old_state': old_state_label,
                'new_state': new_state_label,
                'office_order': self.office_order,
                'file_name': self.file_name
            })

            # 3. Update the Employee Status
            employee.write({'state': self.new_state})