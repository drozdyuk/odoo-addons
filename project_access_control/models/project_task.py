from openerp import fields, models, api, exceptions
import logging

_logger = logging.getLogger(__name__)

class ProjectIssueAccess(models.Model):
    _inherit = "project.task"

    @api.multi
    def unlink(self):
        for record in self:
            access_control_rules_id = self.env['project.access.control.rules'].search([('user_id.id','=', self.env.user.id), ('project_id.id','=',record.project_id.id)])
            if access_control_rules_id and access_control_rules_id.tasks_delete == False:
                raise exceptions.Warning(('Error'), ('You cannot delete an task that you did not have access.'))
        return super(ProjectIssueAccess, self).unlink()

    @api.multi
    def write(self, vals):
        for record in self:
            access_control_rules_id = self.env['project.access.control.rules'].search([('user_id.id','=', self.env.user.id), ('project_id.id','=',record.project_id.id)])
            if access_control_rules_id and access_control_rules_id.tasks_write == False:
                raise exceptions.Warning(('Error'), ('You cannot edit an task that you did not have access.'))
        return super(ProjectIssueAccess, self).write(vals)

    @api.model
    def create(self, vals):
        access_control_rules_id = self.env['project.access.control.rules'].search([('user_id.id','=', self.env.user.id), ('project_id.id','=', vals['project_id'])])
        if access_control_rules_id and access_control_rules_id.tasks_create == False:
            _logger.info('000000000000000000000000000000 %s', access_control_rules_id)
            raise exceptions.Warning(('Error'), ('You cannot create an task that you did not have access.'))
        return super(ProjectIssueAccess, self).create(vals)