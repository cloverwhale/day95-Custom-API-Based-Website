from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    stock_symbol = StringField("股票代號", validators=[DataRequired()])
    submit = SubmitField("搜尋")
