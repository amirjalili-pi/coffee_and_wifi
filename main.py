from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# Exercise:
class CafeForm(FlaskForm):
    name = StringField(label="Cafe Name", validators=[DataRequired()])
    location_url = StringField(label="Location URL", validators=[DataRequired(), URL()])
    open_time = StringField(label="Open Time", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating",
                                choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                                         ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")], validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi Rating",
                              choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"),
                                       ("💪💪💪💪💪", "💪💪💪💪💪")],
                              validators=[DataRequired()])
    power_outlet = SelectField(label="Location URL",
                               choices=[("✘", "✘"), ("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"), ("☕☕☕☕☕", "☕☕☕☕☕")],
                               validators=[DataRequired()])
    submit = SubmitField(label="Add")


# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["get", "post"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            print("True")
            with open('cafe-data.csv', 'a') as fd:
                fd.write(f"\n{form.name.data},{form.location_url.data},{form.open_time.data},{form.closing_time.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_outlet.data}")
            return redirect("/")
        # Exercise:
        # Make the form write a new row into cafe-data.csv
        # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv') as data:
        cafe_data = data.read().splitlines()
    cafe_key = cafe_data[0].split(",")
    cafes_info = cafe_data[1:]
    cafe_list = []
    for info in cafes_info:
        cafe_list.append(dict(zip(cafe_key, info.split(","))))
    print(cafe_list)
    return render_template('cafes.html', cafes=cafe_list)


if __name__ == '__main__':
    app.run(debug=True)
