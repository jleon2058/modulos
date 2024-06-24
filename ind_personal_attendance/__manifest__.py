# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Indomin Personal Attendance",
    "author": "Javier Yataco",
    "version": "16.0.1.1.0",
    "summary": "Asistencia del personal de Indomin ",
    "category": "Attendance",
    "depends": ["base","mail"],
    "data": [
        "security/attendance_security.xml",
        "security/ir.model.access.xml",
        "views/attendance_menu_views.xml",
        "views/analytic_account_views.xml",
        # "views/employee_views.xml",
        "views/res_users_views.xml",
        "views/task_views.xml",
        "views/component_views.xml",
        "views/marcaciones_views.xml",
        "views/finish_all_tasks.xml",
    ],
    "demo": [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    'auto_install': False,
}