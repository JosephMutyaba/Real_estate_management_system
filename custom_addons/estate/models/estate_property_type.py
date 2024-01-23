from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'This defines the type for the estate property'
    _order = "name"

    name = fields.Char(string='name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This name is already used, try another one')
    ]
