import logging
from openerp import fields, models, api

_logger = logging.getLogger(__name__)

class ProjectAccessControlRules(models.Model):

    _name = 'project.access.control.rules'

    #name = fields.Char(string='Name')

    user_id  = fields.Many2one('res.users', string='User', readonly=True)

    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade', readonly=True)

    tasks_create  = fields.Boolean(string='Tasks Create', default=True)
    tasks_write   = fields.Boolean(string='Tasks Write', default=True)
    tasks_delete  = fields.Boolean(string='Tasks Delete')
    issues_create = fields.Boolean(string='Issues Create', default=True)
    issues_write  = fields.Boolean(string='Issues Write', default=True)
    issues_delete = fields.Boolean(string='Issues Delete')

'''
class ProjectAccessControlList(models.Model):

    _name = 'project.access.control.list'


    @api.multi
    def _getUserId(self):
        current_id = self.env.context.get('params').get('id')

        _logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX %s', current_id)

        access_control_list_id = self.env['project.access.control.list'].search([('project_id.id', '=', current_id)])
        _logger.info('0000000000000000000000000000000 %s', access_control_list_id)

        user_ids = []
        for recs in access_control_list_id:
            user_ids.append(recs.user_id.id)

        domain = [('id', 'not in', user_ids)]
        _logger.info('1111111111111111111111111111111 %s', domain)
        return domain

    @api.multi
    def _getUserId(self):
        current_id = self.env.context
        _logger.info('000000000000000000000000000000 %s', current_id)
        return current_id


    @api.onchange('user_id') # if these fields are changed, call method
    def _check_change(self):
        _logger.info('1111111111111111111111111111111 %s', self.env.context)


        access_control_list_id = self.env['project.access.control.list'].search([('project_id.id', '=', current_id)])
        user_ids = []
        for recs in access_control_list_id:
            user_ids.append(recs.user_id.id)

        domain = {'domain':{'user_id': [('id', 'not in', user_ids)]}}

        return domain


    auto_server_action_filters = fields.One2many(comodel_name='ir.filters', inverse_name='crm_scenario_action_id', string='Auto Server Action Filter')
    user_id  = fields.Many2one('res.users', string='User', required=True)
    rules_id = fields.Many2one('project.access.control.rules', string='Rules', required=True)

    project_id = fields.Many2one('project.project', ondelete='cascade')

    '''