from odoo import fields, models


class Inherited(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", string="Properties",
                                   domain="[('salesperson','=',id)]")
