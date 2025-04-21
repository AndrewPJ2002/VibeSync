from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import delete
from sqlalchemy.sql import select
from database import db

from models import Playlist, Song, User
from spotify import get_track, search_tracks

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("index.html")


def get_user(username: str) -> User | None:
    row = db.session.execute(select(User).where(User.username == username)).first()
    if row is None:
        return None

    return row.User


def get_playlist(id: str | int) -> Playlist | None:
    row = db.session.execute(select(Playlist).where(Playlist.id == id)).first()
    if row is None:
        return None

    return row.Playlist


@views.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:  # Prevent logged-in users from seeing login page
        return redirect(url_for("views.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username is None or password is None:
            return render_template("login.html")

        user = get_user(username)

        if user is not None and user.check_password(
            password
        ):  # Ensure this function is properly implemented
            session["user_id"] = user.id  # Store user ID in session
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid credentials, try again.", "danger")

    return render_template("login.html")


@views.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:  # Prevent logged-in users from seeing login page
        return redirect(url_for("views.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username is not None and password is not None and get_user(username) is None:
            new_user = User()
            new_user.username = username
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("views.home"))

    return render_template("registration.html")


@views.route("/logout")
def logout():
    session.pop("user_id", None)  # Remove user from session
    flash("Logged out successfully!", "info")
    return redirect(url_for("views.home"))


@views.route("/all-playlists")
def user_playlists():
    if "user_id" not in session:
        return redirect(url_for("views.login"))

    lists = (
        db.session.execute(
            select(Playlist).where(Playlist.creator_id == session["user_id"])
        )
        .scalars()
        .all()
    )

    return render_template("playlists.html", playlists=lists)


@views.route("/playlist/<int:playlist_id>")
def show_playlist(playlist_id):
    plist = get_playlist(playlist_id)
    if plist is None:
        return "playlist not found", 404

    if "user_id" in session:
        owner = plist.creator_id == session["user_id"]
    else:
        owner = False

    return render_template("playlist.html", playlist=plist, owner=owner)


@views.route("/create-playlist", methods=["GET", "POST"])
def user_create_playlist():
    if "user_id" not in session:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        name = request.form.get("name")

        if name is not None:
            row = db.session.execute(
                select(Playlist).where(Playlist.name == name)
            ).first()

            if row is None:
                plist = Playlist()
                plist.name = name
                plist.creator_id = session["user_id"]
                db.session.add(plist)
                db.session.commit()

                return redirect(url_for("views.user_playlists"))

    return render_template("create-playlist.html")


@views.route("/playlist/delete/<int:playlist_id>", methods=["POST"])
def user_delete_playlist(playlist_id):
    if "user_id" not in session:
        return redirect(url_for("views.home"))

    plist = get_playlist(playlist_id)
    if plist is None:
        return "playlist not found", 404

    if plist.creator_id != session["user_id"]:
        return "forbidden", 403

    db.session.execute(delete(Playlist).where(Playlist.id == playlist_id))
    db.session.commit()

    return redirect(url_for("views.user_playlists"))


@views.route("/modify-playlist/<int:playlist_id>")
@views.route("/modify-playlist/<int:playlist_id>/<action>", methods=["GET", "POST"])
def user_modify_playlist(playlist_id, action=None):
    if "user_id" not in session:
        return redirect(url_for("views.login"))

    plist = get_playlist(playlist_id)
    if plist is None:
        return "playlist not found", 404

    if plist.creator_id != session["user_id"]:
        return "forbidden", 403

    return render_template("modify-playlist.html", playlist=plist, action=action)


@views.route("/song/search", methods=["POST"])
def search_song():
    name = request.form.get("name")
    print(name)
    playlist_id = request.form.get("playlist_id")

    if name is None or playlist_id is None or "user_id" not in session:
        return redirect(url_for("views.home"))

    plist = get_playlist(playlist_id)

    if plist is None or plist.creator_id != session["user_id"]:
        return redirect(url_for("views.home"))

    tracks = search_tracks(name)

    return render_template("search.html", songs=tracks, playlist=plist)


@views.route("/playlist/add/<int:playlist_id>", methods=["POST"])
def add_song(playlist_id):
    if "user_id" not in session:
        return redirect(url_for("views.home"))

    spotify_id = request.form.get("spotify_id")

    if spotify_id is None:
        return "forbidden", 403

    plist = get_playlist(playlist_id)

    if plist is None:
        return "playlist not found", 404

    if plist.creator_id != session["user_id"]:
        return "forbidden", 403

    row = db.session.execute(select(Song).where(Song.spotify_id == spotify_id)).first()
    if row is None:
        song = get_track(spotify_id)
        db.session.add(song)
        db.session.commit()
    else:
        song = row.Song

    plist.songs.append(song)
    db.session.commit()

    return redirect(url_for("views.show_playlist", playlist_id=plist.id))


@views.route("/playlist/remove/<int:playlist_id>", methods=["POST"])
def remove_song(playlist_id):
    if "user_id" not in session:
        return redirect(url_for("views.home"))

    spotify_id = request.form.get("spotify_id")

    if spotify_id is None:
        return "forbidden", 403

    plist = get_playlist(playlist_id)

    if plist is None:
        return "playlist not found", 404

    for song in plist.songs:
        if song.spotify_id == spotify_id:
            plist.songs.remove(song)
            db.session.commit()
            break

    return redirect(url_for("views.show_playlist", playlist_id=plist.id))
