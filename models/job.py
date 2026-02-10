from odoo import models, fields

class HrJob(models.Model):
    _inherit = 'hr.job'

    state = fields.Selection([
            ('draft', 'Draft'),
            ('recruit', 'Recruiting'),
            ('closed', 'Closed'),
        ], default='draft', tracking=True)

    uni_location_id = fields.Many2one('university.job.location', string="Job Location")