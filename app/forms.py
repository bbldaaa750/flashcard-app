from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DeckForm(FlaskForm):
    title = StringField('Название колоды', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Создать')
