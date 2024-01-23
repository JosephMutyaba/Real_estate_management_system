from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'property tags'
    _order = "name"

    name = fields.Char(string='name', required=True)
    color = fields.Integer(string='Color')
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Already in use, please choose another tag name')
    ]
