from flask import Flask
from flask import render_template
from flask import request

from weather_api import (get_current_weather)
from recommender import get_current_season, get_recommendation_genres
from spotify_api import get_top_tracks

app = Flask(__name__)

