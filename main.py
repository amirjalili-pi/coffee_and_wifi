from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/place"
mongo = PyMongo(app)
mongo_cafes = mongo.db.cafes
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

"""this form is for adding new cafes"""


# Exercise:
class CafeForm(FlaskForm):
    name = StringField(label="Cafe Name", validators=[DataRequired()])
    location_url = StringField(label="Location URL", validators=[DataRequired(), URL()])
    open_time = StringField(label="Open Time", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating",
                                choices=[("✘", "✘"), ("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"),
                                         ("☕☕☕☕☕", "☕☕☕☕☕")], validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi Rating",
                              choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"),
                                       ("💪💪💪💪", "💪💪💪💪"),
                                       ("💪💪💪💪💪", "💪💪💪💪💪")],
                              validators=[DataRequired()])
    power_outlet = SelectField(label="Location URL",
                               choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"),
                                        ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                                        ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")],
                               validators=[DataRequired()])
    submit = SubmitField(label="Add")


"""this form is for editing cafe data"""


class CafeEditForm(FlaskForm):
    coffee_rating = SelectField(label="Coffee Rating",
                                choices=[("✘", "✘"), ("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"),
                                         ("☕☕☕☕☕", "☕☕☕☕☕")], validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi Rating",
                              choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"),
                                       ("💪💪💪💪", "💪💪💪💪"),
                                       ("💪💪💪💪💪", "💪💪💪💪💪")],
                              validators=[DataRequired()])
    power_outlet = SelectField(label="Location URL",
                               choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"),
                                        ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                                        ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")],
                               validators=[DataRequired()])
    submit = SubmitField(label="Add")


# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------
# with open('cafe-data.csv') as data:
#     cafe_data = data.read().splitlines()
#     cafe_key = cafe_data[0].split(",")
#     cafes_info = cafe_data[1:]
#     cafe_list = []
#     for info in cafes_info:
#         cafe_list.append(dict(zip(cafe_key, info.split(","))))
#     for cafe in cafe_list:
#         mongo_cafes.insert_one({"name": cafe["Cafe Name"], "location": cafe["Location"],
#                                 "open_t": cafe["Open"], "close_t": cafe["Close"],
#                                 "coffee_rate": cafe["Coffee"],
#                                 "wifi_rate": cafe["Wifi"], "power_rate": cafe["Power"]})

"""home page"""


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


"""cafe list page"""


@app.route('/cafes')
def cafes():
    all_cafes = mongo_cafes.find()
    return render_template('cafes.html', cafes=all_cafes)


"""this method create a record in mongo db"""


@app.route('/add', methods=["get", "post"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            print("True")
            mongo_cafes.insert_one({"name": form.name.data, "location": form.location_url.data,
                                    "open_t": form.open_time.data, "close_t": form.closing_time.data,
                                    "coffee_rate": form.coffee_rating.data,
                                    "wifi_rate": form.wifi_rating.data, "power_rate": form.power_outlet.data})
            # with open('cafe-data.csv', 'a') as fd:
            #     fd.write(f"\n{form.name.data},
            #     {form.location_url.data},{form.open_time.data},{form.closing_time.data},
            #     {form.coffee_rating.data},{form.wifi_rating.data},{form.power_outlet.data}")
            flash("You've been created on record", "success")
            return redirect("/cafes")
        # Exercise:
        # Make the form write a new row into cafe-data.csv
        # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


"""this method update a record in mongo db"""


@app.route("/edit", methods=['get', 'post'])
def edit_cafe():
    form = CafeEditForm()
    cafe_id = request.args.get("pk")
    if request.method == "POST":
        if form.validate_on_submit():
            mongo_cafes.update_one({"_id": ObjectId(cafe_id)}, {"$set": {"coffee_rate": form.coffee_rating.data,
                                                                         "wifi_rate": form.wifi_rating.data,
                                                                         "power_rate": form.power_outlet.data}})
            flash("You've been updated on record", "info")
            return redirect("/cafes")
    cafe = mongo_cafes.find_one({"_id": ObjectId(cafe_id)})
    return render_template("edit.html", form=form, cafe=cafe)


"""this method delete record's"""


@app.route("/delete", methods=["get", "post"])
def delete_cafe():
    cafe_id = request.args.get("pk")
    mongo_cafes.delete_one({"_id": ObjectId(cafe_id)})
    flash("You've been deleted one record", "danger")
    return redirect("/cafes")
    # return render_template("index.html", message="You've been deleted one record", msg_class="danger")


if __name__ == '__main__':
    app.run(debug=True)
