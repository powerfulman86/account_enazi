# -*- coding: utf-8 -*-

from odoo import models, fields, api
from decimal import Decimal
from num2words import num2words


class ResCurrency(models.Model):
    _inherit = "res.currency"

    currency_subunit_label = fields.Char(translate=True)
    currency_unit_label = fields.Char(translate=True)

    def _compute_amount_words(self, total_amount):
        total_amount_words = ''
        currency = self.env.company.currency_id
        amount = int(total_amount)
        amount_decimal = int(total_amount * 1000 % 1000)
        try:
            lang = self.env['res.lang'].search([('iso_code', '=', 'ar')], limit=1)
            unit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                      ('src', '=', currency.currency_unit_label)], limit=1)

            subunit = self.env['ir.translation'].search([('lang', '=', lang.code),
                                                         ('src', '=', currency.currency_subunit_label)], limit=1)
            if not unit:
                src = self.env['ir.translation'].search([('value', '=', currency.currency_unit_label)], limit=1).src

                unit = self.env['ir.translation'].search([('lang', '=', lang.code), ('src', '=', src)], limit=1)
                if not unit:
                    unit = self.env['ir.translation'].search([('src', '=', src)], limit=1)
            if not subunit:
                src = self.env['ir.translation'].search([('value', '=', currency.currency_subunit_label)], limit=1).src

                subunit = self.env['ir.translation'].search([('lang', '=', lang.code), ('src', '=', src)], limit=1)
                if not subunit:
                    subunit = self.env['ir.translation'].search([('src', '=', src)], limit=1)
            if unit and subunit and unit.value and subunit.value:
                if amount and amount_decimal:
                    total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                         (unit.value or unit.src) + ', ' + num2words(
                        Decimal(str(amount_decimal)), lang='ar') + ' ' + (subunit.value or subunit.src)
                elif amount or not total_amount:
                    total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                         (unit.value or unit.src)
                elif amount_decimal:
                    total_amount_words = num2words(Decimal(str(amount_decimal)),
                                                   lang='ar') + ' ' + (subunit.value or subunit.src)

            elif currency.currency_unit_label and currency.currency_subunit_label:
                if amount and amount_decimal:
                    total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                         (currency.currency_unit_label) + ', ' + num2words(
                        Decimal(str(amount_decimal)), lang='ar') + ' ' + (currency.currency_subunit_label)
                elif amount or not total_amount:
                    total_amount_words = num2words(Decimal(str(amount)), lang='ar') + ' ' + \
                                         (currency.currency_unit_label)
                elif amount_decimal:
                    total_amount_words = num2words(Decimal(str(amount_decimal)),
                                                   lang='ar') + ' ' + (currency.currency_subunit_label)
            else:
                total_amount_words = num2words(Decimal(str(total_amount)), lang='ar') + ' ' + str(currency.symbol)
        except NotImplementedError:
            total_amount_words = num2words(Decimal(str(total_amount)), lang='en') + ' ' + str(
                currency.currency_id.symbol)

        return total_amount_words
