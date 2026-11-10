from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class FeedbackForm(FlaskForm):
    user_name = StringField("Ім'я", validators=[DataRequired(), Length(max=50)])
    user_email = EmailField("Електронна пошта", validators=[DataRequired(), Email()])
    topic_category = SelectField(
        "Категорія",
        choices=[('tech', 'Технічна'), ('general', 'Загальна')],
    )
    user_message = TextAreaField("Повідомлення", validators=[DataRequired()])

    def validate_user_message(self, field):
        if len(field.data.split()) < 3:
            raise ValidationError("Повідомлення має містити хоча б 3 слова.")
