{
    "name": "Project Portfolio",
    "license": "LGPL-3",
    "version": "1.0.0",
    "summary": "Portfolio management for projects (departmental visibility)",
    "author": "You",
    "depends": ["project", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/portfolio_record_rules.xml",
        "views/portfolio_views.xml",
        "views/project_project_search_inherit.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
}
