# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from . import estate_property_offer
from . import estate_property_tag
from . import estate_property_type
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.users", string="Buyer")
    salesperson_id = fields.Many2one("res.partner", string="Salesperson", default=lambda self:self.env.user)

    active = fields.Boolean(default=True)        
    name = fields.Char(required=True, default="Unknown")
    postcode = fields.Integer(default=7500)
    description = fields.Text()
    date_availability = fields.Date(copy=False, default=datetime.datetime.now() + datetime.timedelta(days=90))
    # fields.Date(copy=True, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    living_area = fields.Integer(default=55)
    garden_area = fields.Integer(default=10)
    bedrooms = fields.Integer(default=2)
    garden = fields.Boolean()
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
            record.best_price = max(record.mapped('offer_ids.price'))

    @api.onchange("partner_id")
        def _onchange_partner_id(self):
            self.name = "Document for %s" % (self.partner_id.name)
            self.description = "Default description for %s" % (self.partner_id.name)