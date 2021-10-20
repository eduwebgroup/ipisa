# -*- coding: utf-8 -*-

from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class Ipisa(models.Model):
    _inherit = 'sale.coupon.reward'

    reward_type = fields.Selection(selection_add=[('extra_product', 'Extra Product')])

    def name_get(self):
        result = []
        reward_names = super(Ipisa, self).name_get()
        reward_string = ''
        for reward in self:
            reward_string = reward.reward_product_id.name
        free_extra_product_reward_ids = self.filtered(lambda reward: reward.reward_type == 'extra_product').ids
        for res in reward_names:
            result.append((res[0], res[0] in free_extra_product_reward_ids and reward_string or res[1]))
        return result

