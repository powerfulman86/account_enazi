# -*- coding: utf-8 -*-
# from odoo import http


# class AccountEnazi(http.Controller):
#     @http.route('/account_enazi/account_enazi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_enazi/account_enazi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_enazi.listing', {
#             'root': '/account_enazi/account_enazi',
#             'objects': http.request.env['account_enazi.account_enazi'].search([]),
#         })

#     @http.route('/account_enazi/account_enazi/objects/<model("account_enazi.account_enazi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_enazi.object', {
#             'object': obj
#         })
