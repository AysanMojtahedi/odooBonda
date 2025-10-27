from odoo import _, models, fields, api


class ProjectPortfolio(models.Model):
    _name = "project.portfolio"
    _description = _("Project Portfolio")

    name = fields.Char(required=True)
    department_id = fields.Many2one(
        "hr.department",
        string=_("Department"),
        required=True,
    )
    leader_id = fields.Many2one("res.users", string=_("Leader"))
    allow_cross_visibility = fields.Boolean(default=False)
    project_ids = fields.One2many(
        "project.project",
        "portfolio_id",
        string=_("Projects"),
    )
    project_count = fields.Integer(
        string=_("Number of Projects"), compute="_compute_project_count"
    )

    manager_ids = fields.Many2many(
        "res.users",
        string=_("Managers"),
        relation="portfolio_manager_rel",
        column1="portfolio_id",
        column2="user_id",
    )

    @api.depends("project_ids")
    def _compute_project_count(self):
        for portfolio in self:
            portfolio.project_count = len(portfolio.project_ids)

    def action_add_project(self):
        return {
            "name": _("Add Project"),
            "type": "ir.actions.act_window",
            "res_model": "portfolio.project.line",
            "view_mode": "form",
            "target": "new",
            "context": {"default_portfolio_id": self.id},
        }


class PortfolioProjectLine(models.TransientModel):
    _name = "portfolio.project.line"
    _description = _("Line to add projects to portfolio")

    portfolio_id = fields.Many2one("project.portfolio", string=_("Portfolio"))
    project_id = fields.Many2one("project.project", string=_("Project"), required=True)

    def action_add_to_portfolio(self):
        for line in self:
            if line.project_id:
                line.project_id.portfolio_id = line.portfolio_id
        return {"type": "ir.actions.act_window_close"}
