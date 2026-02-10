from odoo import models, fields

class EmployeeMedicalHistory(models.Model):
    _name = 'employee.medical.history'
    _description = 'Employee Medical History'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    disease_name = fields.Char("Disease/Injury Name")
    is_surgery = fields.Boolean("Surgery Performed?")
    hospital_name = fields.Char("Hospital Name")
    admission_date = fields.Date("Admission Date")
    discharge_date = fields.Date("Discharge Date")
    severity = fields.Selection([
        ('low', 'Low'), 
        ('medium', 'Medium'), 
        ('high', 'High'), 
        ('critical', 'Critical')
    ], string="Severity")

class EmployeeFamilyMember(models.Model):
    _name = 'employee.family.member'
    _description = 'Employee Family Member'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    name = fields.Char("Name", required=True)
    relation = fields.Selection([
        ('spouse', 'Spouse'), 
        ('child', 'Child'), 
        ('parent', 'Parent')
    ], required=True)
    dob = fields.Date("Date of Birth")
    cnic = fields.Char("CNIC")
    phone = fields.Char("Phone")
    status = fields.Selection([('alive', 'Alive'), ('deceased', 'Deceased')], default='alive')

class EmployeeEducation(models.Model):
    _name = 'employee.education'
    _description = 'Educational Background'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    institute_id = fields.Many2one('university.institute', string="Institute", required=True)
    degree_id = fields.Many2one('university.degree', string="Degree", required=True)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    score = fields.Char("Marks/CGPA")

class EmployeePublication(models.Model):
    _name = 'employee.publication'
    _description = 'Research and Publications'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    title = fields.Char("Title", required=True)
    journal = fields.Char("Journal/Conference")
    date_published = fields.Date("Date Published")
    link = fields.Char("URL")