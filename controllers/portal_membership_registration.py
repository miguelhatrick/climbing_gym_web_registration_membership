# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import json
import pdb

from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo import fields, http, _
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression


class CustomerPortalSchool(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortalSchool, self)._prepare_portal_layout_values()
        _partner = request.env.user.partner_id

        course = request.env['climbing_gym.membership_registration']
        course_count = course.search_count([
            ('state', 'in', ['active']),
            ('partner_id', '=', _partner.id),
            # ('state', 'in', ['sale', 'done'])
        ])

        values.update({
            'membership_registration_count': course_count,
        })
        return values

    @http.route(['/my/membership_registration', '/my/membership_registration/page/<int:page>'], type='http',
                auth="user",
                website=True)
    def portal_my_membership_registration(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        _course = request.env['climbing_gym.membership_registration']

        domain = [
            ('state', 'in', ['active', 'closed'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Creation date'), 'order': 'create_date desc'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('climbing_gym.membership_registration', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        quotation_count = _course.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/membership_registration",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        courses = _course.search(domain, order=sort_order, limit=self._items_per_page,
                                 offset=pager['offset'])

        request.session['my_membership_registration_history'] = courses.ids[:100]

        values.update({
            'date': date_begin,
            'courses': courses.sudo(),
            'partner': partner,
            'page_name': 'membership_registration',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/membership_registration',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("climbing_gym_school.portal_my_membership_registration", values)
