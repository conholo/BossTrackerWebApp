from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError

from bosstracker.models import Boss


class RegisterBossForm(FlaskForm):
    bossname = StringField("Name", validators=[DataRequired()])
    submit = SubmitField('Add Boss')

