# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from . import estate_property_type
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.user", string="Buyer")
    salesperson_id = fields.Many2one("res.partner", string="Salesperson")

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
    garden_orientation = fields.Selection([('north','North'), ('south','South'),('east','East'),('west','West')])
    state = fields.Selection(
        [('new','New'), ('offerReceived','Offer Received'),('offerAccepted','Offer Accepted'),('sold','Sold'), ('cancelled','Cancelled')],
        default="new",
        copy=False,
        required=True
    )