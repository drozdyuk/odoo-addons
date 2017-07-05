# -*- coding: utf-8 -*-

import logging
from openerp import fields, models, api
#from openerp.exceptions import Warning
#from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

#if str(object.subject) != '' and object.type == 'email':
#    self.pool['crm.lead'].browse(cr, uid, object.res_id).update({'stopped': True})

class CrmMailScenario(models.Model):

    _name = 'crm.mail.scenario'

    name = fields.Char(string='Name', required='True')
    scenario_action = fields.One2many(comodel_name='crm.mail.scenario.action', inverse_name='crm_mail_scenario_id', string='Scenario Actions')

class CrmMailScenarioAction(models.Model):

    _name = 'crm.mail.scenario.action'

    sequence = fields.Integer(string='Sequence')
    #active = fields.Boolean(string='Active')
    name = fields.Char(string='Name', required='True')
    delay_value = fields.Integer(string='Delay value', required='True')
    delay_units = fields.Selection(selection=[('minutes', 'Minutes'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month')], string='Delay Units', required='True')
    auto_server_action = fields.One2many(comodel_name='base.action.rule', inverse_name='crm_scenario_action_id', string='Auto Server Action')
    auto_server_action_filters = fields.One2many(comodel_name='ir.filters', inverse_name='crm_scenario_action_id', string='Auto Server Action Filter')
    server_action = fields.One2many(comodel_name='ir.actions.server', inverse_name='crm_scenario_action_id', string='Server Action')
    crm_mail_scenario_id = fields.Many2one(comodel_name='crm.mail.scenario', string='Scenario')
    crm_mail_template = fields.Many2one(comodel_name='email.template', string='Mail tpl', domain=[('model_id','=','crm.lead')], required='True')

    @api.multi
    def get_field_id(self, field, model):
        field_id = self.env['ir.model.fields'].search([('name', '=', field), ('model_id.model', '=', model)])
        return field_id.id
    @api.multi
    def get_model_id(self, model):
        model_id = self.env['ir.model'].search([('model', '=', model)])
        return model_id.id

    @api.multi
    def get_record_id(self, model, name):
        rec_id = self.env[model].search([('name', '=', name)])
        return rec_id.id

    @api.model
    def create(self, vals):
        #Write your logic here

        mail_message_content = self.crm_mail_template.browse(vals['crm_mail_template']).body_html

        vals_ir_filters = {
            'name': 'CAM filters' + ' ' + vals['name'],
            'model_id': 'crm.lead',
            'domain': [['stopped', '!=', True], ['auto_mailing_scenario', '=', vals['crm_mail_scenario_id']]],
        }
        ir_filters = self.env['ir.filters'].create(vals_ir_filters)

        vals_mail_message_create = [
            (0, 0, {'col1': self.get_field_id('model', 'mail.message'), 'type':'value', 'value':'crm.lead'}),
            (0, 0, {'col1': self.get_field_id('res_id', 'mail.message'), 'type':'equation', 'value':'object.id'}),
            (0, 0, {'col1': self.get_field_id('body', 'mail.message'), 'type':'value', 'value': mail_message_content}),
            (0, 0, {'col1': self.get_field_id('type', 'mail.message'), 'type':'value', 'value':'email'}),
            (0, 0, {'col1': self.get_field_id('partner_ids', 'mail.message'), 'type':'equation', 'value':'[(4, object.partner_id.id)]'}),
            (0, 0, {'col1': self.get_field_id('subtype_id', 'mail.message'), 'type':'value', 'value': self.get_record_id('mail.message.subtype', 'Crm Auto Mailing')}),
        ]

        vals_server_action_create = {
            'name': 'CAM server action' + ' ' + vals['name'],
            'model_id': self.get_model_id('crm.lead'),
            'state': 'object_create',
            'use_create': 'new_other',
            'crud_model_id': self.get_model_id('mail.message'),
            'fields_lines': vals_mail_message_create,
        }

        vals_auto_server_action_create = {
            'name': 'CAM auto server action' + ' ' + vals['name'],
            'model_id': self.get_model_id('crm.lead'),
            'kind': 'on_time',
            'trg_date_id': self.get_field_id('scenario_start_date', 'crm.lead'),
            'filter_id': ir_filters.id,
            'trg_date_range': vals['delay_value'],
            'trg_date_range_type': vals['delay_units'],
            'server_action_ids': [(0, 0, vals_server_action_create)],
        }

        vals['auto_server_action'] = [(0, 0, vals_auto_server_action_create)]

        #_logger.info('777777777777777777777777777777 %s', vals)

        res = super(CrmMailScenarioAction, self).create(vals)

        ir_filters.update({'crm_scenario_action_id': res.id})

        ir_actions_server = self.env['ir.actions.server'].search([('id','=',res.auto_server_action.server_action_ids.id)])
        ir_actions_server.update({'crm_scenario_action_id': res.id})

        return res
