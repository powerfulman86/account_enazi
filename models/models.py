# -*- coding: utf-8 -*-

from odoo import models, fields, api
from decimal import Decimal
from num2words import num2words
from odoo.tools import float_is_zero


class ResCurrency(models.Model):
    _inherit = "res.currency"

    currency_subunit_label = fields.Char(translate=True)
    currency_unit_label = fields.Char(translate=True)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends('invoice_line_ids', 'currency_id', 'company_id', 'invoice_date')
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for record in self:
            amount = int(record.amount_total)
            amount_decimal = int(record.amount_total * 100 % 100)

            try:
                lang = self.env['res.lang'].search([('iso_code', '=', 'ar')], limit=1)
                print("Lang = ", lang.code)
                unit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                          ('src', '=', record.currency_id.currency_unit_label)],
                                                         limit=1)

                subunit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                             ('src', '=',
                                                              record.currency_id.currency_subunit_label)], limit=1)
                if not unit:
                    src = self.env['ir.translation'].search([
                        ('value', '=', record.currency_id.currency_unit_label)], limit=1).src

                    unit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                              ('src', '=', src)],
                                                             limit=1)
                    if not unit:
                        unit = self.env['ir.translation'].search([('src', '=', src)], limit=1)
                if not subunit:
                    src = self.env['ir.translation'].search([
                        ('value', '=', record.currency_id.currency_subunit_label)], limit=1).src

                    subunit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                                 ('src', '=', src)],
                                                                limit=1)
                    if not subunit:
                        subunit = self.env['ir.translation'].search([('src', '=', src)], limit=1)

                print("Units = ", record.currency_id.currency_unit_label, record.currency_id.currency_subunit_label)
                print("Units 2 = ", subunit.value, subunit.src)
                if unit and subunit and unit.value and subunit.value:
                    if amount and amount_decimal:
                        record.total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                                    (unit.value or unit.src) + ', ' + num2words(
                            Decimal(str(amount_decimal)),
                            lang='ar') + ' ' + (subunit.value or subunit.src)
                    elif amount or not record.amount_total:
                        record.total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                                    (unit.value or unit.src)
                    elif amount_decimal:
                        record.total_amount_words = num2words(Decimal(str(amount_decimal)),
                                                              lang='ar') + ' ' + (
                                                            subunit.value or subunit.src)

                elif record.currency_id.currency_unit_label and record.currency_id.currency_subunit_label:
                    if amount and amount_decimal:
                        record.total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                                    (record.currency_id.currency_unit_label) + ', ' + num2words(
                            Decimal(str(amount_decimal)),
                            lang='ar') + ' ' + (record.currency_id.currency_subunit_label)
                    elif amount or not record.amount_total:
                        record.total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                                    (record.currency_id.currency_unit_label)
                    elif amount_decimal:
                        record.total_amount_words = num2words(Decimal(str(amount_decimal)),
                                                              lang='ar') + ' ' + (
                                                        record.currency_id.currency_subunit_label)
                else:
                    record.total_amount_words = num2words(Decimal(str(record.amount_total)),
                                                          lang='ar') + ' ' + str(record.currency_id.symbol)
            except NotImplementedError:
                print("2222222222222222222222")
                record.total_amount_words = num2words(Decimal(str(record.amount_total)), lang='en') + ' ' + str(
                    record.currency_id.symbol)

        return res

    total_amount_words = fields.Char(string="Amount in Words", compute='_compute_amount', store=True)
