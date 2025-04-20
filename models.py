from typing import List
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import db

# this is to encrypt passwords
bcrypt = Bcrypt()


# define a user table
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    # hashes password and then decodes it into a string for storage
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # checks the password with hashed password and then returns true or false
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # used for debugging
    def __repr__(self):
        return f"<User {self.username}>"


playlist_songs = Table(
    "playlist_songs",
    db.Model.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id")),
    Column("song_id", Integer, ForeignKey("songs.id")),
)


class Song(db.Model):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    spotify_id: Mapped[str] = mapped_column(nullable=True)
    artist: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)


class Playlist(db.Model):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    creator: Mapped[User] = relationship()
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    songs: Mapped[List[Song]] = relationship(secondary=playlist_songs)
