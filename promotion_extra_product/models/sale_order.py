

# -*- coding: utf-8 -*-

from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_reward_line_values(self, program):
        if program.reward_type == 'extra_product':
            print('rew', self._get_reward_values_extra(program))
            return self._get_reward_values_extra(program)
        else:
            return super(SaleOrder, self)._get_reward_line_values(program)

    def _get_reward_values_extra(self, program):

        return [{
            'name': program.reward_product_id.name,
            'product_id': program.discount_line_product_id.id,
            'price_unit': 0.0,
            'product_uom_qty': 1.0,
            'product_uom': program.discount_line_product_id.uom_id.id,
            'is_reward_line': True,
            'tax_id': [(4, tax.id, False) for tax in program.discount_line_product_id.taxes_id],
            'coupon_program_id': program.id
        }]

    def _update_existing_reward_lines(self):
        '''Update values for already applied rewards'''

        def update_line(order, lines, values):
            '''Update the lines and return them if they should be deleted'''
            lines_to_remove = self.env['sale.order.line']
            # Check commit 6bb42904a03 for next if/else
            # Remove reward line if price or qty equal to 0
            if values['product_uom_qty'] and values['price_unit']:
                lines.write(values)
            elif program.reward_type == 'extra_product':
                lines.write(values)
            else:
                if program.reward_type != 'free_shipping':
                    # Can't remove the lines directly as we might be in a recordset loop
                    lines_to_remove += lines
                else:
                    values.update(price_unit=0.0)
                    lines.write(values)
            return lines_to_remove

        self.ensure_one()
        order = self
        applied_programs = order._get_applied_programs_with_rewards_on_current_order()
        for program in applied_programs:
            values = order._get_reward_line_values(program)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id)
            if program.reward_type == 'discount' and program.discount_type == 'percentage':
                lines_to_remove = lines
                # Values is what discount lines should really be, lines is what we got in the SO at the moment
                # 1. If values & lines match, we should update the line (or delete it if no qty or price?)
                # 2. If the value is not in the lines, we should add it
                # 3. if the lines contains a tax not in value, we should remove it
                for value in values:
                    value_found = False
                    for line in lines:
                        # Case 1.
                        if not len(set(line.tax_id.mapped('id')).symmetric_difference(
                                set([v[1] for v in value['tax_id']]))):
                            value_found = True
                            # Working on Case 3.
                            lines_to_remove -= line
                            lines_to_remove += update_line(order, line, value)
                            continue
                    # Case 2.
                    if not value_found:
                        order.write({'order_line': [(0, False, value)]})
                # Case 3.
                lines_to_remove.unlink()
            else:
                update_line(order, lines, values[0]).unlink()