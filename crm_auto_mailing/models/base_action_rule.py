import logging
from openerp import fields, models, api

_logger = logging.getLogger(__name__)

class BaseActionRule(models.Model):

    _inherit = 'base.action.rule'

    crm_scenario_action_id = fields.Many2one('crm.mail.scenario.action', ondelete='cascade')
