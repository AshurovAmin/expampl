from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required


from . import app, db

from .models import User, Position, Employee
from .forms import EmployeeForm, PositionForm, UserLoginForm, UserRegisterForm, User, EmployeeUpdateForm


def index():
    students = Employee.query.all()
    return render_template('index.html', students=students)

@login_required
def admin_position_create():
    form = PositionForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_position = Position(
                name=form.name.data,
                department=form.department.data,
                wage=form.wage.data
            )
            db.session.add(new_position)
            db.session.commit()
            flash('Position успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении курса произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('position_create.html', form=form)



@login_required
def admin_employee_create():
    form = EmployeeForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_employee = Employee(
                name=form.name.data,
                inn=form.inn.data,
            )
            db.session.add(new_employee)
            db.session.commit()
            flash('Сoтрудник успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении курса произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('employee_create.html', form=form)

@login_required
def admin_employee_detail():
    pass


@login_required
def admin_employee_update(student_id):
    employee = Employee.query.get(student_id)
    form = EmployeeUpdateForm(meta={'csrf': False}, obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Студент успешно обновлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При обновлении Студента произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


@login_required
def admin_course_delete(employee_id):
    employee = Employee.query.get(employee_id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Курс успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('employee_delete.html', employee=employee)



def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован!', 'success!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка{". ".join(text_list)}', 'Ошибка!')

    return render_template('form.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему, Успех!')
                return redirect(url_for('index'))
            else:
                flash('Неверные логин и пароль', 'Ошибка!')
    return render_template('form.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))