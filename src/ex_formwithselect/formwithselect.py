from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, SubmitField

# Minimal app config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah'


# Flask-WTF form
class SimpleForm(FlaskForm):
    radio_field = RadioField('RadioA', choices=[('one', '1'), ('two', '2')])
    select_field = SelectField('SelectA', choices=[('blue', 'Blue chosen'), ('red', 'Red chosen')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def form_submit():
    form = SimpleForm()
    if form.validate_on_submit():
        select_value = form.select_field.data
        radio_value = form.radio_field.data
        result = f'You chose select: {select_value}, radio: {radio_value}'
        return render_template("form.html", form=form, result=result)
    return render_template("form.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
