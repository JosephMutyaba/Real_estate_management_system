from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOfffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offers'
    _order = "id desc"

    price = fields.Float(string='Price', required=True)
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0)', 'Offer Price must be greater than 0')
    ]

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False, readonly=True, string='Status')
    partner_id = fields.Many2one('res.partner', string='Partner Id', required=True)
    property_id = fields.Many2one('estate.property', string='Property Id', required=True, ondelete='cascade')

    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline',
                                store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = (create_date + timedelta(days=record.validity)).date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    # def action_accept(self):
    #     # Logic for accepting the offer goes here
    #     self.write({'status': 'accepted'})
    #     return True

    def action_refuse(self):
        # Logic for refusing the offer goes here
        self.write({'status': 'refused'})
        return True

    # def action_accept(self):
    #     for offer in self:
    #         # Logic for accepting the offer goes here
    #         if offer.property_id.status != 'new':
    #             raise UserError("An offer can only be accepted for a property with status 'new'.")
    #
    #         # Ensure only one offer can be accepted for a given property
    #         existing_accepted_offer = self.env['estate.property.offer'].search([
    #             ('property_id', '=', offer.property_id.id),
    #             ('status', '=', 'accepted'),
    #         ], limit=1)
    #
    #         if existing_accepted_offer:
    #             raise UserError("Another offer has already been accepted for this property.")
    #
    #         # Accept the offer and update the property
    #         offer.write({'status': 'accepted'})
    #         offer.property_id.accept_offer(offer)
    #
    #     return True
    #

    def action_accept(self):
        for offer in self:
            # Logic for accepting the offer goes here
            if offer.property_id.status != 'offer received':
                raise UserError("An offer can only be accepted for a property with status 'new'.")

            # Ensure only one offer can be accepted for a given property
            existing_accepted_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted'),
            ], limit=1)

            if existing_accepted_offer:
                raise UserError("Another offer has already been accepted for this property.")

            seventy_percent = (70 / 100) * offer.property_id.expected_price
            if offer.price < seventy_percent:
                raise UserError("You cannot accept an offer less than 70% of expected price")

            # Accept the offer and update the property
            offer.write({'status': 'accepted'})

    # @api.constrains(property_id.selling_price)
    # def check_selling_price(self):
    #     for record in self:
    #         existing_accepted_offer = self.env['estate.property.offer'].search([
    #             ('property_id', '=', record.property_id.id),
    #             ('status', '=', 'accepted'),
    #         ], limit=1)
    #         if record.

    @api.model
    def create(self, vals):
        """Override the create method to set the property state and check for existing offers."""
        property_id = vals.get('property_id')
        amount = vals.get('price')

        # Check if the property has existing offers with higher amounts
        existing_offers = self.search([('property_id', '=', property_id), ('price', '>', amount)])
        if existing_offers:
            raise models.ValidationError("Cannot create offer with lower amount than existing offer(s).")

        # Set the property state to 'Offer Received'
        property_model = self.env['estate.property']
        property_record = property_model.browse(property_id)
        property_record.write({'status': 'offer received'})

        # Continue with the standard create process
        return super().create(vals)

    @api.model
    def update(self, vals):
        """Override the create method to set the property state and check for existing offers."""
        property_id = vals.get('property_id')
        amount = vals.get('price')

        # Check if the property has existing offers with higher amounts
        existing_offers = self.search([('property_id', '=', property_id), ('price', '>', amount)])
        if existing_offers:
            raise models.ValidationError("Cannot create offer with lower amount than existing offer(s).")

        # # Set the property state to 'Offer Received'
        # property_model = self.env['estate.property']
        # property_record = property_model.browse(property_id)
        # property_record.write({'status': 'offer received'})

        # Continue with the standard create process
        return super().create(vals)
