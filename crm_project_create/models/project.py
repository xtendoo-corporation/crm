from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    lead_id = fields.Many2one(
        "crm.lead",
        string="Opportunity",
    )
