# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from . import estate_property_offer
from . import estate_property_tag
from . import estate_property_type
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "sequence, id desc"

    sequence = fields.Integer('Sequence', default=1, help="Used to order properties.")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self:self.env.user)

    active = fields.Boolean(default=True)        
    name = fields.Char(required=True, default="Unknown")
    postcode = fields.Integer(default=7500)
    description = fields.Text()
    date_availability = fields.Date(copy=False, default=datetime.datetime.now() + datetime.timedelta(days=90))
    # fields.Date(copy=True, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    living_area = fields.Integer(default=55)
    bedrooms = fields.Integer(default=2)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north','North'), ('south','South'),('east','East'),('west','West')])
    state = fields.Selection(
        [('new','New'), ('offerReceived','Offer Received'),('offerAccepted','Offer Accepted'),('sold','Sold'), ('cancelled','Cancelled')],
        default="new",
        copy=False,
        required=True
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped('offer_ids.price'), default=0)

    @api.onchange("garden")
    def _onchange_garden_info(self):
        if self.garden == True:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0

    def cancel_btn(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('It is not possible to cancel a SOLD property')
                return
            record.state = 'cancelled'
        return True

    def sold_btn(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('It is not possible to sell a CANCELLED property')
                return
            record.state = 'sold'
            return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Property sold, well done!'
                    }
                }


        @api.constrains('selling_price','expected_price')
        def _check_date_end(self):
            for record in self:
                if record.selling_price <= 0 or record.expected_price <= 0:
                    raise ValidationError("All prices must be POSITIVEand greater than zero!")