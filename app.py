from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, InputRequired
import json
import os
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap(app)

DATA_FILE = 'feedback.json'

# Проверяем, существует ли файл JSON, если нет, создаем пустой
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваша почта', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class CalculatorForm(FlaskForm):
    num1 = FloatField('Число 1', validators=[InputRequired()])
    num2 = FloatField('Число 2', validators=[InputRequired()])
    operation = SelectField('Выберите операцию', choices=[('+', '+'), ('-', '-'), ('*', '*'), ('/', '/')],
                            validators=[InputRequired()])
    submit = SubmitField('Рассчитать')


class CalculatorForm2(FlaskForm):
    num1 = FloatField('Число 1', validators=[InputRequired()])
    operation2 = SelectField('Выберите операцию', choices=[('x^2', 'x^2'), ('sqrt(x)', 'sqrt(x)'), ('log(x)', 'log(x)'),
                                                           ('exp(x)', 'exp(x)')],
                             validators=[InputRequired()])
    submit = SubmitField('Рассчитать')


def read_feedback():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []


def write_feedback(feedbacks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'one':
            return redirect(url_for('calc2'))
        elif choice == 'two':
            return redirect(url_for('calc'))
    return render_template('choose.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    form = CalculatorForm()
    result = None

    if form.validate_on_submit():
        num1 = float(form.num1.data)
        num2 = float(form.num2.data)
        operation = form.operation.data

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Деление на ноль невозможно"

    return render_template('calc.html', title='Калькулятор', form=form, result=result)


@app.route('/calc2', methods=['GET', 'POST'])
def calc2():
    form = CalculatorForm2()
    result = None

    if form.validate_on_submit():
        num1 = float(form.num1.data)
        operation = form.operation2.data

        if operation == 'x^2':
            result = math.pow(num1, 2)
        elif operation == 'sqrt(x)':
            result = math.sqrt(num1)
        elif operation == 'log(x)':
            result = math.log(num1)
        elif operation == 'exp(x)':
            result = math.exp(num1)

    return render_template('calc2.html', title='Калькулятор', form=form, result=result)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_data = {
            'name': form.name.data,
            'email': form.email.data,
            'message': form.message.data
        }
        feedbacks = read_feedback()
        feedbacks.append(feedback_data)
        write_feedback(feedbacks)
    return render_template('feedback.html', form=form, title="Обратная связь")


if __name__ == '__main__':
    app.run()
