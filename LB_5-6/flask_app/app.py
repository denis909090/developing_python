from flask import Flask, render_template, flash, redirect, url_for

from forms import FeedbackForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask-insecure-lab-key-change-me'


@app.route('/')
def home_page():
    context_data = {
        'page_title': 'Головна сторінка Flask',
        'news_items': ['Оновлення системи', 'Нові правила', 'Знижки на послуги'],
        'active_users': 150,
    }
    return render_template('home.html', **context_data)


@app.route('/form', methods=['GET', 'POST'])
def feedback_page():
    form = FeedbackForm()
    if form.validate_on_submit():
        flash('Ваше повідомлення успішно надіслано!', 'success')
        return redirect(url_for('feedback_page'))

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
