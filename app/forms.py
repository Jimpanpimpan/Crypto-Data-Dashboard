from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=80)])
