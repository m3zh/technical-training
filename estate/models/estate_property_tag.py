# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    '''
    type = fields.Selection(
        [('house','House'), ('appartement','Appartement'),('castle','Castle'),('office','Office'), ('chalet','Chalet'), ('tent', 'Tent')],
        default="house",
        copy=False,
        required=True
    )
    '''