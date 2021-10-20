# -*- coding: utf-8 -*-
# from odoo import http


# class DraftInvoice(http.Controller):
#     @http.route('/draft_invoice/draft_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/draft_invoice/draft_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('draft_invoice.listing', {
#             'root': '/draft_invoice/draft_invoice',
#             'objects': http.request.env['draft_invoice.draft_invoice'].search([]),
#         })

#     @http.route('/draft_invoice/draft_invoice/objects/<model("draft_invoice.draft_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('draft_invoice.object', {
#             'object': obj
#         })
