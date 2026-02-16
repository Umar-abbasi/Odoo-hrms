from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date

class UniversityEmployee(models.Model):
    _inherit = 'hr.employee'

    # --- Basic Details ---
    university_tag_ids = fields.Many2many(
        'university.employee.tag', 
        string="Employee Category",
        help="Select categories like Faculty, Staff, Army, Office, etc."
    )
    
    # --- IDENTIFIERS (Removed required=True to allow Draft state) ---
    emp_code = fields.Char("Employee Code", copy=False)
    biometric_code = fields.Char("Biometric Code", copy=False)

    cnic = fields.Char("CNIC")
    father_name = fields.Char(string="Father's Name")
    dual_nationality = fields.Boolean("Dual Nationality")
    domicile = fields.Char("Domicile")
    religion_id = fields.Many2one('university.religion', string="Religion")
    age = fields.Integer(string="Age", compute="_compute_age")
    
    # --- UPDATED STATE WORKFLOW ---
    state = fields.Selection([
        ('draft', 'Draft'),                 # 1. Fill Info
        ('code_generated', 'ID Generated'), # 2. Codes Confirmed
        ('profile_locked', 'Locked'),       # 3. Read-Only Check
        ('active', 'Active'),               # 4. Live
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
        ('compulsory_retired', 'Compulsory Retired'),
        ('terminated', 'Terminated'),
        ('removed', 'Removal from Service'),
        ('dismissed', 'Dismissal from Service'),
        ('deceased', 'Deceased'),
        ('archived', 'Archived')
    ], string="Status", default='draft', tracking=True)

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
    status_history_ids = fields.One2many('employee.status.history', 'employee_id', string="Status History")
    medical_history_ids = fields.One2many('employee.medical.history', 'employee_id', string="Medical History")
    family_member_ids = fields.One2many('employee.family.member', 'employee_id', string="Family Members")
    education_ids = fields.One2many('employee.education', 'employee_id', string="Education")
    publication_ids = fields.One2many('employee.publication', 'employee_id', string="Publications")
    
    last_appraisal_date = fields.Date("Last Appraisal")
    active_appraisal = fields.Boolean("Appraisal In Progress")

    # =========================================================
    # WORKFLOW BUTTON ACTIONS
    # =========================================================

    def action_generate_code(self):
        """ 
        Step 1 -> 2: Validate Biometric Code and Generate Employee Code.
        """
        for rec in self:
            if not rec.biometric_code:
                raise UserError("Please enter a Biometric Code first (Manually or from Device).")
            
            # Ensure it is numeric
            if not rec.biometric_code.isdigit():
                raise UserError("Biometric Code must contain only numbers.")

            # Auto-Generate Employee Code (Pad with Zeros)
            rec.emp_code = rec.biometric_code.zfill(4)
            
            # Move to Next Stage
            rec.state = 'code_generated'

    def action_lock_profile(self):
        """ 
        Step 2 -> 3: Lock the profile so no changes can be made.
        """
        for rec in self:
            if not rec.emp_code or not rec.biometric_code:
                raise UserError("Cannot lock profile without Employee Codes.")
            rec.state = 'profile_locked'

    def action_activate_employee(self):
        """ 
        Step 3 -> 4: Make the employee Active.
        """
        self.write({'state': 'active'})

    def action_reset_draft(self):
        """ 
        Correction Button: Go back to Draft to fix mistakes.
        """
        self.write({'state': 'draft'})

    # =========================================================
    # CONSTRAINTS & LOGIC
    # =========================================================

    _sql_constraints = [
        ('unique_biometric_code', 'unique(biometric_code)', 'Biometric Code must be unique!'),
        ('unique_emp_code', 'unique(emp_code)', 'Employee Code must be unique!')
    ]

    @api.constrains('biometric_code')
    def _check_biometric_numeric(self):
        for rec in self:
            if rec.biometric_code and not rec.biometric_code.isdigit():
                raise ValidationError("Biometric Code must contain only numbers!")

    @api.onchange('biometric_code')
    def _onchange_biometric_code(self):
        """ Real-time update for manual entry """
        if self.biometric_code and self.biometric_code.isdigit():
            self.emp_code = self.biometric_code.zfill(4)

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            if rec.birthday:
                today = date.today()
                rec.age = today.year - rec.birthday.year - ((today.month, today.day) < (rec.birthday.month, rec.birthday.day))
            else:
                rec.age = 0