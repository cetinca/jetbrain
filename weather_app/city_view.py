from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from weather_api import get_weather
from city_model import City

city_blueprint = Blueprint("cities", __name__)


def find_cards():
    cards = City.find_all()
    for card in cards:
        weather = get_weather(card["city"])
        card["temp"] = weather["temp"]
        card["state"] = weather["state"]
    return cards


@city_blueprint.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        # if not session.get("city", None):
        #     session["city"] = os.urandom(24)
        return render_template("index.html", cards=find_cards())
        # return render_template("index.html", cards=cards, s=session["city"])

    if request.method == "POST":
        # if not session.get("city", None):
        #     return render_template("index.html")
        _id = request.form.get("id", None)
        city = request.form.get("city_name", None)
        weather = get_weather(city)
        if not city or not weather:
            flash("The city doesn't exist!")
        else:
            City(city).save_to_db() if not City.find_by_city(city) else flash(
                "The city has already been added to the list!")
        return redirect("/")


@city_blueprint.route('/delete/<city_id>', methods=['GET', 'POST', 'DELETE'])
def delete_city(city_id):
    if city_id:
        city = City.find_by_id(city_id)
        if city:
            city.delete()
            return redirect("/")
    flash("The city doesn't exist!")
    return redirect("/")
