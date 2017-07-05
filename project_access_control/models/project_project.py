# -*- coding: utf-8 -*-

import logging
from openerp import fields, models, api

_logger = logging.getLogger(__name__)

class ProjectMembersAccess(models.Model):

    _inherit = 'project.project'

    user_access_control_rules = fields.One2many(comodel_name='project.access.control.rules', inverse_name='project_id', string='Users')

    @api.multi
    def write(self, vals):

        #_logger.info('000000000000000000000000000000 %s', self.members)

        before = self.members
        res = super(ProjectMembersAccess, self).write(vals)
        after = self.members

        if len(before) > len(after):
            deleted_rules = []
            deleted_rules_id = []
            result = list(set(before) ^ set(after))
            for record in result:
                unlink_id = self.env['project.access.control.rules'].search([('user_id','=',record.id), ('project_id','=',self.id)])
                record_item = (2, unlink_id.id)
                deleted_rules.append(record_item)
            self.user_access_control_rules = deleted_rules
            self.write({'user_access_control_rules': deleted_rules})

        elif len(before) < len(after):
            created_rules = []
            result = list(set(before) ^ set(after))
            for record in result:
                vals_user_access_control_rules = {
                    'user_id': record.id
                }
                record_item = (0, 0, vals_user_access_control_rules)
                created_rules.append(record_item)
            self.write({'user_access_control_rules': created_rules})

        return res

    @api.model
    def create(self, vals):
        res = super(ProjectMembersAccess, self).create(vals)

        created_rules = []
        for record in res.members:
            vals_user_access_control_rules = {
                'user_id': record.id
            }
            record_item = (0, 0, vals_user_access_control_rules)
            created_rules.append(record_item)

        res.update({'user_access_control_rules': created_rules})

        return res


    '''
    @api.onchange('user_access_control_list') # if these fields are changed, call method
    def _check_change(self):

        current_id = self.env.context.get('params').get('id')
        _logger.info('000000000000000000000000000000 %s', current_id)
        access_control_list_id = self.env['project.access.control.list'].search([('project_id.id', '=', current_id)])
        user_ids = []
        for recs in access_control_list_id:
            user_ids.append(recs.user_id.id)

        domain = {'domain':{'user_access_control_list.user_id': [('id', 'not in', user_ids)]}}

        _logger.info('1111111111111111111111111111111 %s', domain)
        return domain
    '''