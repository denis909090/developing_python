from django import forms
from django.core.exceptions import ValidationError


class FeedbackForm(forms.Form):
    user_name = forms.CharField(label="Ім'я", max_length=50)
    user_email = forms.EmailField(label="Електронна пошта")
    topic_category = forms.ChoiceField(
        label="Категорія",
        choices=[('tech', 'Технічна'), ('general', 'Загальна')],
    )
    user_message = forms.CharField(label="Повідомлення", widget=forms.Textarea)

    def clean_user_message(self):
        text_data = self.cleaned_data.get('user_message')
        if len(text_data.split()) < 3:
            raise ValidationError("Повідомлення має містити хоча б 3 слова.")
        return text_data
