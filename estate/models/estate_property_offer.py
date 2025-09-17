# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import ValidationError, UserError
from . import estate_property


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer"
    _order = "price desc"

    price = fields.Float(required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    status = fields.Selection(
        [('accepted','Accepted'), ('refused','Refused'),('pending','Pending')],
        default="pending",
        copy=False
    )

    def accept_btn(self):
        for record in self.property_id.offer_ids:
            if record.status == 'accepted':
                raise UserError('An offer was already accepted for this real estate, SORRY!')
                return False
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Offer accepted, well done!'
                    }
                }
        for record in self.property_id.offer_ids:
            if record.status != 'accepted':
                record.status = 'refused'
        return True

    def refuse_btn(self):
        for record in self:
            record.status = 'refused'
        return True

        @api.constrains('price')
        def _check_date_end(self):
            for record in self:
                if record.price <= 0:
                    raise ValidationError("All prices must be POSITIVEand greater than zero!")
