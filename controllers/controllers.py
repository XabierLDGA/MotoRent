# -*- coding: utf-8 -*-
# from odoo import http


# class Motorent(http.Controller):
#     @http.route('/motorent/motorent', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/motorent/motorent/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('motorent.listing', {
#             'root': '/motorent/motorent',
#             'objects': http.request.env['motorent.motorent'].search([]),
#         })

#     @http.route('/motorent/motorent/objects/<model("motorent.motorent"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('motorent.object', {
#             'object': obj
#         })
