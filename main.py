from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import os
import dotenv

import requests

dotenv.load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///video-games-ranking.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# TOKENS ENV THEM!!!
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
access_token = os.getenv('access_token')


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Game(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'<Game {self.title}>'


# with app.app_context():
#     db.drop_all()
#     db.create_all()


# Create Form for editing entries
class UpdateGameForm(FlaskForm):
    rating = FloatField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField('Update')


class AddGameForm(FlaskForm):
    game_title = StringField(label='Game Title', validators=[DataRequired()])
    submit = SubmitField('Search Game')


@app.route("/")
def home():
    # Get all entries from the DB to display on homepage.
    results = db.session.execute(db.select(Game).order_by(Game.rating))
    list_of_games = results.scalars().all()

    for i in range(len(list_of_games)):
        list_of_games[i].ranking = len(list_of_games) - i
    db.session.commit()

    return render_template("index.html", list_of_games=list_of_games)


@app.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddGameForm()

    # Redirect to search for video game
    if add_form.validate_on_submit():
        game_title = add_form.game_title.data
        response = requests.post('https://api.igdb.com/v4/search',
                                 **{'headers': {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {access_token}'},
                                    'data': f'fields game,name; search "{game_title}"; limit 50;'})
        response.raise_for_status()
        search_result_by_title = response.json()
        # print(search_result_by_title)
        return render_template('select.html', searched_games=search_result_by_title)

    else:
        return render_template('add.html', form=add_form)


@app.route('/edit/<game_id>', methods=['GET', 'POST'])
def edit(game_id):
    update_form = UpdateGameForm()

    if update_form.validate_on_submit():
        game_to_update = db.session.execute(db.select(Game).where(Game.id == game_id)).scalar()
        game_to_update.rating = update_form.rating.data
        game_to_update.review = update_form.review.data
        db.session.commit()
        return redirect('/')
    else:
        game = db.session.execute(db.select(Game).where(Game.id == game_id)).scalar()
        return render_template('edit.html', game=game, form=update_form)  # :^)


@app.route('/delete/<game_id>')
def delete(game_id):
    game_to_delete = db.session.execute(db.select(Game).where(Game.id == game_id)).scalar()
    db.session.delete(game_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/select/<game_ref_id>')
def select(game_ref_id):
    # API Call - Get Game by ID
    response = requests.post('https://api.igdb.com/v4/games',
                             **{'headers': {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {access_token}'},
                                'data': f'fields cover, name, rating, summary, release_dates; where id = {game_ref_id};'})
    response.raise_for_status()
    selected_game_data = (response.json())[0]

    game_title = selected_game_data['name']
    try:
        release_year_id = selected_game_data['release_dates'][0]
    except IndexError:
        release_year_id = 0

    description = selected_game_data['summary']
    cover_id = selected_game_data['cover']

    year_response = requests.post('https://api.igdb.com/v4/release_dates',
                                  **{'headers': {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {access_token}'},
                                     'data': f'fields y; where id = {release_year_id};'})

    cover_response = requests.post('https://api.igdb.com/v4/covers',
                              **{'headers': {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {access_token}'},
                                 'data': f'fields checksum, height, url, width; where id = {cover_id};'})

    year = (year_response.json())[0]['y']
    cover_url = (cover_response.json())[0]['url']
    cover_url = cover_url.replace('t_thumb', 't_cover_big')
    new_game = Game(
        title=game_title,
        year=year,
        description=description,
        rating=10,
        ranking=1,
        review="N/A",
        img_url=cover_url
    )
    db.session.add(new_game)
    db.session.commit()

    this_entry = db.session.execute(db.select(Game).where(Game.title == game_title)).scalar()
    return redirect(url_for("edit", game_id=this_entry.id))


if __name__ == '__main__':
    app.run(debug=True)
