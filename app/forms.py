from flask_wtf import FlaskForm
import wtforms as wf
from . import app

from .models import Employee, User, Position


class PositionForm(FlaskForm):
    name = wf.StringField(label='Введите свое имя: ', validators=[
        wf.validators.DataRequired()
    ])
    wage = wf.IntegerField(label='Введите zh: ', validators=[
        wf.validators.DataRequired(),
        wf.validators.NumberRange(min=0)
    ])
    department = wf.StringField(label='Введите департамент: ', validators=[
        wf.validators.DataRequired()
    ])

def employees_choices():
    employees_choices = []
    with app.app_context():
        employees = Employee.query.all()
        for employee in employees:
            employees_choices.append((employee.id, employee.position))
    return employees_choices

class EmployeeForm(FlaskForm):
    name = wf.StringField(label='Введите свое имя: ', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.IntegerField(label='Введите зарплату: ', validators=[
        wf.validators.DataRequired()
    ])
    position_id = wf.SelectField(label="Выбери позицию: ", choices=employees_choices)

    def validate_inn(self, field):
        if Employee.query.filter_by(inn=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким inn уже существует')

    def validate_inn_numbers(self, field):
        if len(field.data) < 14: # > 14 ToDO
            raise wf.ValidationError('Длина пароля должна быть минимум 14 символов')

class EmployeeUpdateForm(FlaskForm):
    name = wf.StringField(label='ФИО Студента')
    inn = wf.SelectField(label="Курс", choices=employees_choices)




class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password_2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password_2.data:
            self.password_2.errors.append('Пароли должны совпадать')
            return False
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким username уже существует')
