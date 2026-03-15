from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    theme = StringField(validators=[DataRequired()])
    age = StringField(validators=[DataRequired()])
    duration = StringField(validators=[DataRequired()])
    instruments = StringField(validators=[DataRequired()])
    submit = SubmitField('Подобрать')