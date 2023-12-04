from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, InputRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:15931@localhost/my_database'
db = SQLAlchemy(app)
Bootstrap(app)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


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


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


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


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(feedback)
        db.session.commit()
    return render_template('feedback.html', form=form, title="Обратная связь")


if __name__ == '__main__':
    app.run()
