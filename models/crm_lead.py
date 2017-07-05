import logging
from openerp import fields, models, api

_logger = logging.getLogger(__name__)

class CrmLeadMAiling(models.Model):

    _inherit = 'crm.lead'

    auto_mailing_scenario = fields.Many2one(comodel_name='crm.mail.scenario', string='Scenario')
    stopped = fields.Boolean(string='Stopped')
    scenario_start_date = fields.Datetime(string='Scenario Start Date')