from flask import Blueprint, render_template, flash
from datetime import datetime
from eggList.models import ListaProductos
main = Blueprint('main',__name__)


@main.route("/home")
@main.route("/")
def home():


    return render_template('main/home.html')
