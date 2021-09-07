# -*- coding: utf-8 -*-
import logging
import pdb
from datetime import datetime, timedelta, date, timezone
from typing import List

import odoo
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MembershipRegistration(models.Model):
    """Career"""
    _name = 'climbing_gym.membership_registration'
    _description = 'Membership registration'
    _inherit = ['mail.thread']

    status_selection = [('pending', "Pending"), ('approve', "Approved"), ('cancel', "Cancelled")]

    civil_status_selection = [('married', "Married"), ('single', "Single"), ('other', "Other")]

    name = fields.Char('Name', compute='_generate_name'
                       )
    description = fields.Char('Description')

    contact_firstname = fields.Char('Requester firstname')

    contact_lastname = fields.Char('Requester lastname')

    partner_id = fields.Many2one('res.partner', string='Member', required=True, index=True, track_visibility=True)

    membership_id = fields.Many2one('climbing_gym.membership', string='Membership type', index=True,
                                    track_visibility=True)

    email = fields.Char('email')

    birthdate = fields.Date('Birthdate', track_visibility=True)

    civil_status = fields.Selection(civil_status_selection, 'Civil status', default='single', track_visibility=True)

    # main_id_category_id
    # main_id_number
    # civil_partner
    # home_address
    # profesion
    # workplace_company
    # work_address
    # phone
    # cellphone

    attachment_personal_ids = fields.Many2many('ir.attachment', 'membership_registration_rel',
                                               'membership_registration_id',
                                               'personal_id', 'Personal ID')

    attachment_photo_ids = fields.Many2many('ir.attachment', 'membership_registration_rel',
                                            'membership_registration_id',
                                            'personal_id', 'Personal ID')

    obs = fields.Text('Observations')
    state = fields.Selection(status_selection, 'Status', default='pending', track_visibility=True)

    course_ids = fields.One2many('climbing_gym_school.course', inverse_name='career_id',
                                 string='Courses', readonly=True)

    @api.multi
    def action_revive(self):
        for _map in self:
            _map.state = 'pending'

    @api.multi
    def action_approve(self):
        for _map in self:
            _map.state = 'approve'

            # TODO: Check for missing data



    @api.multi
    def action_cancel(self):
        for _map in self:
            _map.state = 'cancel'

    def _generate_name(self):
        # pdb.set_trace()
        for _map in self:
            _map.name = "REG-%s" % (_map.id if _map.id else '')
