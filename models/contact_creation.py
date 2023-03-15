from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SurveyContact(models.Model):

    _name = 'contact.creation'

    relation_id = fields.Many2one('survey.survey')
    questions_id = fields.Many2one('survey.question', string='Question',domain="[('survey_id', '=', relation_id)]")
    contacts_id = fields.Many2one("ir.model.fields", string='Contact Fields',domain="[('model', '=', 'res.partner')]")

    @api.onchange('contacts_id')
    def onchange_question_id_field(self):
        self.relation_id = self.relation_id._origin


class Survey(models.Model):

    _inherit = "survey.survey"
    contact_creation_ids = fields.One2many('contact.creation', 'relation_id')



class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):

        result={}
        for rec in self.survey_id.contact_creation_ids:
            for res in self.user_input_line_ids:
                if res.question_id in rec.questions_id:
                    result.update({
                        rec.contacts_id.name : res.display_name
                    })
        if result['name'] == 'Skipped':
            raise ValidationError("name field is mandatory")
        else:
            self.env['res.partner'].create(result)
        super(SurveyUserInput, self)._mark_done()