from app import app

from . import views


app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/admin/position/create', view_func=views.admin_position_create, methods=['GET', 'POST'])
app.add_url_rule('/admin/employee/create', view_func=views.admin_employee_create, methods=["GET", "POST"])
app.add_url_rule('/admin/employee/<int:employee_id>/update', view_func=views.admin_employee_update, methods=['POST', 'GET'])





app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)