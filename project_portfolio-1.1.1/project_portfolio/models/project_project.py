from odoo import _, models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    portfolio_id = fields.Many2one(
        "project.portfolio",
        string=_("Portfolio"),
    )

    def action_remove_from_portfolio(self):
        for project in self:
            project.portfolio_id = False

    def action_open_project_form(self):
        self.ensure_one()
        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "res_id": self.id,
            "view_mode": "form",
        }

    portfolio_project_count = fields.Integer(
        string=_("Projects in Portfolio"),
        compute="_compute_portfolio_project_count",
        store=False,
    )

    @api.depends("portfolio_id")
    def _compute_portfolio_project_count(self):
        for project in self:
            if project.portfolio_id:
                project.portfolio_project_count = self.env[
                    "project.project"
                ].search_count([("portfolio_id", "in", project.portfolio_id.ids)])
            else:
                project.portfolio_project_count = 0

    def action_view_portfolio_projects(self):
        self.ensure_one()
        if not self.portfolio_id:
            return {"type": "ir.actions.act_window_close"}
        return {
            "name": _("Projects in Portfolio"),
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "tree,form",
            "domain": [("portfolio_id", "in", self.portfolio_id.ids)],
        }

    progress = fields.Float(
        string=_("Progress"),
        compute="_compute_progress",
        store=False,
    )

    def _compute_progress(self):
        for project in self:
            last_update = self.env["project.update"].search(
                [("project_id", "=", project.id)], order="create_date desc", limit=1
            )
            project.progress = last_update.progress if last_update else 0.0
