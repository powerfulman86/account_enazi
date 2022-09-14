# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends('invoice_line_ids', 'currency_id', 'company_id', 'invoice_date')
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()

        for record in self:
            try:
                record.total_amount_words = record.currency_id._compute_amount_words(record.amount_total)
            except NotImplementedError:
                record.total_amount_words = ''

        return res

    total_amount_words = fields.Char(string="Amount in Words", compute='_compute_amount', store=True)
