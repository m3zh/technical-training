# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    description = fields.Text()      
    type = fields.Selection(
        [('house','House'), ('appartement','Appartement'),('castle','Castle'),('office','Office'), ('chalet','Chalet'), ('tent', 'Tent')],
        default="house",
        copy=False,
        required=True
    )