from odoo import models, fields, api
from datetime import date

class UniversityEmployee(models.Model):
    _inherit = 'hr.employee'

    # --- Basic Details ---
    university_tag_ids = fields.Many2many(
        'university.employee.tag', 
        string="Employee Category",
        help="Select categories like Faculty, Staff, Army, Office, etc."
    )
    
    emp_code = fields.Char("Employee Code")
    biometric_code = fields.Char("Biometric Code")
    cnic = fields.Char("CNIC")
    father_name = fields.Char(string="Father's Name")
    dual_nationality = fields.Boolean("Dual Nationality")
    domicile = fields.Char("Domicile")
    religion_id = fields.Many2one('university.religion', string="Religion")
    age = fields.Integer(string="Age", compute="_compute_age")
    
    # --- Status Workflow ---
    state = fields.Selection([
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
        ('compulsory_retired', 'Compulsory Retired'),
        ('terminated', 'Terminated'),
        ('removed', 'Removal from Service'),
        ('dismissed', 'Dismissal from Service'),
        ('deceased', 'Deceased'),
        ('archived', 'Archived')
    ], string="Current Status", default='active', tracking=True)

    # --- Work Info ---
    scale_id = fields.Many2one('university.payscale', string="Pay Scale")
    scale_stage = fields.Char("Stage")
    increment_date = fields.Date("Next Increment Date")
    
    # --- Private Info Extensions ---
    personal_email = fields.Char("Personal Email")
    disability = fields.Boolean("Disability")
    disability_nature_id = fields.Many2one('university.disability', string="Nature of Disability")

    # --- HR Settings Extensions ---
    first_contract_date = fields.Date("First Contract Date")
    regularization_date = fields.Date("Regularization Date")
    confirmation_date = fields.Date("Confirmation Date")
    date_of_leaving = fields.Date("Date of Leaving")
    operation_area = fields.Char("Operation Area")
    registration_number = fields.Char("Registration Number")

    # --- Pay Scale Details ---
    basic_pay_type = fields.Selection([('initial', 'Initial'), ('running', 'Running')], string="Basic Pay Type")
    personal_pay = fields.Float("Personal Pay")
    manual_gross = fields.Float("Manual Gross")
    manual_tax = fields.Float("Manual Tax")

    # --- RELATIONAL FIELDS ---
    medical_history_ids = fields.One2many('employee.medical.history', 'employee_id', string="Medical History")
    family_member_ids = fields.One2many('employee.family.member', 'employee_id', string="Family Members")
    education_ids = fields.One2many('employee.education', 'employee_id', string="Education")
    publication_ids = fields.One2many('employee.publication', 'employee_id', string="Publications")
    
    # --- Appraisal Placeholder ---
    last_appraisal_date = fields.Date("Last Appraisal")
    active_appraisal = fields.Boolean("Appraisal In Progress")

    status_history_ids = fields.One2many('employee.status.history', 'employee_id', string="Status History")
    
    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            if rec.birthday:
                today = date.today()
                rec.age = today.year - rec.birthday.year - ((today.month, today.day) < (rec.birthday.month, rec.birthday.day))
            else:
                rec.age = 0