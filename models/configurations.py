from odoo import models, fields

class UniversityReligion(models.Model):
    _name = 'university.religion'
    _description = 'Religion Configuration'
    _order = 'name'
    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)

class UniversityDisability(models.Model):
    _name = 'university.disability'
    _description = 'Disability Nature'
    _order = 'name'
    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    remarks = fields.Text(string="Remarks / Explanation")

class UniversityInstitute(models.Model):
    _name = 'university.institute'
    _description = 'Institute/University'
    _order = 'name'
    name = fields.Char(string="Institute Name", required=True)
    code = fields.Char(string="Institute Code", required=True, index=True)
    city = fields.Char(string="City")

class UniversityDegree(models.Model):
    _name = 'university.degree'
    _description = 'Educational Degree'
    _order = 'name'
    name = fields.Char(string="Degree Name", required=True)
    code = fields.Char(string="Degree Code", required=True, index=True)

class UniversityPayScale(models.Model):
    _name = 'university.payscale'
    _description = 'Pay Scale (BPS/TTS)'
    _order = 'name'
    name = fields.Char(string="Scale Name", required=True, help="e.g. BPS-17")
    category = fields.Selection([
        ('bps', 'BPS'),
        ('tts', 'TTS'),
        ('fixed', 'Fixed / Contract')
    ], string="Category", required=True)

class UniversityAppointment(models.Model):
    _name = 'university.appointment.type'
    _description = 'Appointment Type'
    name = fields.Char(string="Type", required=True, help="e.g. Regular, Contract")
    code = fields.Char(required=True)

class UniversityJobLocation(models.Model):
    _name = 'university.job.location'
    _description = 'Job Location'
    _order = 'name'
    name = fields.Char(string="Location Name", required=True, help="e.g. North Campus")
    address = fields.Char(string="Address")
    city = fields.Char(string="City")

    _sql_constraints = [
        ('unique_location_name', 'unique(name)', 'Location name must be unique!')
    ]