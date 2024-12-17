# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class CrmCreateProject(models.TransientModel):
    _name = "crm.create.project"
    _description = "Wizart to create Project from Lead/Opportunity"

    project_name = fields.Char()
    project_description = fields.Html()
    lead_id = fields.Many2one("crm.lead")
    duplicate_project_id = fields.Many2one(
        "project.project", string="Duplicate Project"
    )

    def create_project(self):
        if self.duplicate_project_id:
            project = self.duplicate_project_id.copy(
                {
                    "name": self.project_name,
                    "description": self.project_description,
                    "lead_id": self.lead_id.id,
                }
            )
        else:
            project = (
                self.env["project.project"]
                .sudo()
                .create(self._prepare_create_project_values())
            )
        self.lead_id.project_id = project
        project.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": self.lead_id.project_id, "origin": self.lead_id},
            subtype_id=self.env.ref("mail.mt_note").id,
            author_id=self.env.user.partner_id.id,
        )

    def _prepare_create_project_values(self):
        values = {
            "name": self.project_name,
            "description": self.project_description,
            "active": True,
            "allow_billable": True,
        }
        if self.duplicate_project_id:
            values.update(
                {
                    "name": self.project_name,
                    "description": self.project_description,
                    "lead_id": self.lead_id.id,
                    "partner_id": self.lead_id.partner_id.id,
                    "company_id": self.lead_id.company_id.id,
                }
            )
        else:
            values.update(
                {
                    "partner_id": self.lead_id.partner_id.id,
                    "company_id": self.lead_id.company_id.id,
                }
            )
        return values
