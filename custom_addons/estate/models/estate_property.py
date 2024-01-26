from odoo import models, fields, api
from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class RealEstate(models.Model):
    _name = 'estate.property'
    _description = 'This is the estate property table'
    _order = "id desc"

    active = fields.Boolean("Active", default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('canceled', 'Canceled'),
    ], string='Status', default='new', readonly=True, copy=False)

    name = fields.Char(required=True, default="New Home")
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available from', copy=False,
                                    default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price', required=True)
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be greater than 0')
    ]
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False,
                                 compute='_compute_buyer_selling_price')
    best_price = fields.Float(compute="_compute_best_price")

    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    property_type_id = fields.Many2one('estate.property.type', string="Property type")
    tag_ids = fields.Many2many('estate.property.tag', string='Tag', options="{'color_field': 'color'}")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer Id')
    garden_area = fields.Integer(string='Garden Area')

    total_area = fields.Integer(compute="_compute_total")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
        ('other', 'Other'),
    ], string='Garden Orientation', default='other')

    buyer = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True,
                            compute='_compute_buyer_selling_price')
    salesperson = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user.id)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = ''
            self.garden_area = 0

    # compute the total_area
    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    # calculate the best price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            b_price = max(record.offer_ids.mapped('price'), default=0.0)
            record.best_price = b_price

    def button_cancel(self):
        for property_rec in self:
            if property_rec.status == 'sold':
                raise UserError("A sold property cannot be canceled.")
            property_rec.write({'status': 'canceled'})

    def button_sold(self):
        for property_rec in self:
            if property_rec.status == 'cancel':
                raise UserError("A canceled property cannot be set as sold.")
            property_rec.write({'status': 'sold'})

    @api.depends('offer_ids.status', 'offer_ids.partner_id', 'offer_ids.price')
    def _compute_buyer_selling_price(self):
        for rec in self:
            accepted_offers = rec.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if accepted_offers:
                accepted_offer = accepted_offers[0]  # Assuming only one offer can be accepted
                rec.buyer = accepted_offer.partner_id.id
                rec.selling_price = accepted_offer.price
            else:
                rec.buyer = False
                rec.selling_price = 0.2

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for record in self:
            if record.date_availability < datetime.now().date():
                raise ValidationError("The date of availability cannot be in the past.")

    @api.ondelete(at_uninstall=True)
    def _delete_record(self):
        for record in self:
            if record.status not in ('new', 'canceled'):
                raise UserError("Cannot delete property with state other than 'New' or 'Canceled'")

