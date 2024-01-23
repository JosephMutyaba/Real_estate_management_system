from odoo import models, fields, api


class NationalIDApplication(models.Model):
    _name = 'national.id.application'
    _description = 'National ID Application'

    name = fields.Char(string='Full Name', required=True)
    nin = fields.Char(string="NIN", required=True, copy=False)
    dob = fields.Date(string='Date of Birth', required=True)
    address = fields.Text(string='Address', required=True)
    picture = fields.Binary(string='Picture')
    reference_letter = fields.Binary(string='LC Reference Letter')

    stage = fields.Selection([
        ('application', 'Application'),
        ('review', 'Review'),
        ('approved', 'Approved'),
    ], string='Stage', default='application', required=True, tracking=True)

    @api.model_create_multi
    def action_review(self):
        self.write({'stage': 'review'})

    @api.model_create_multi
    def action_approve(self):
        self.write({'stage': 'approved'})
