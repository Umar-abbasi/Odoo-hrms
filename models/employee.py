from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class UniversityEmployee(models.Model):
    _inherit = 'hr.employee'

    # --- Basic Details ---
    university_tag_ids = fields.Many2many('university.employee.tag', string="Employee Category")
    
    # --- IDENTIFIERS ---
    emp_code = fields.Char("Employee Code", copy=False, readonly=True)
    biometric_code = fields.Char("Biometric Code", copy=False, readonly=True)

    cnic = fields.Char("CNIC")
    father_name = fields.Char(string="Father's Name")
    dual_nationality = fields.Boolean("Dual Nationality")
    domicile = fields.Char("Domicile")
    religion_id = fields.Many2one('university.religion', string="Religion")
    age = fields.Integer(string="Age", compute="_compute_age")
    
    # --- UPDATED STATE WORKFLOW ---
    state = fields.Selection([
        ('draft', 'Draft'),                 
        ('profile_locked', 'Locked'),       
        ('active', 'Active'),               
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
    # STRICT SECURITY: PREVENT EDITING WHEN LOCKED/ACTIVE
    # =========================================================
    def write(self, vals):
        """
        Stop ANY edit if the profile is Locked or Active.
        Exception: Allow changing the 'state' (to unlock/activate) and tracking messages.
        """
        # If we are only changing the state (e.g., Locking or Unlocking), allow it.
        if len(vals) == 1 and ('state' in vals or 'message_follower_ids' in vals):
            return super(UniversityEmployee, self).write(vals)

        # For any other change (Name, DOB, Family, etc.), CHECK STATE
        for rec in self:
            if rec.state in ['profile_locked', 'active']:
                raise UserError(_("This profile is LOCKED. You cannot change any information (Personal, Family, HR, etc.) while it is Locked or Active.\n\nPlease click 'Unlock Profile' first."))
        
        return super(UniversityEmployee, self).write(vals)

    # =========================================================
    # BUTTON ACTION: GENERATE CODE
    # =========================================================
    def action_generate_code(self):
        for rec in self:
            if rec.emp_code or rec.biometric_code:
                raise UserError("Codes are already generated!")
            
            # 1. Generate Biometric Code from Sequence
            seq = self.env['ir.sequence'].next_by_code('hr.employee.biometric') or '0'
            rec.biometric_code = seq
            
            # 2. Auto-Generate Employee Code (Pad with Zeros)
            rec.emp_code = rec.biometric_code.zfill(4)

    # =========================================================
    # WORKFLOW BUTTON ACTIONS
    # =========================================================

    def action_lock_profile(self):
        """ Draft -> Locked """
        for rec in self:
            if not rec.emp_code:
                raise UserError("Please click 'Generate Code' before locking the profile.")
        self.write({'state': 'profile_locked'})

    def action_activate_employee(self):
        """ Locked -> Active """
        self.write({'state': 'active'})

    def action_unlock_profile(self):
        """ Moves back to 'draft' so fields become editable. """
        self.write({'state': 'draft'})

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            if rec.birthday:
                today = date.today()
                rec.age = today.year - rec.birthday.year - ((today.month, today.day) < (rec.birthday.month, rec.birthday.day))
            else:
                rec.age = 0