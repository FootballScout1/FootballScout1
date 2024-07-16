#!/usr/bin/python3
import datetime
import random
from models import scout
from models.post import Post
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.club import Club
from models.player import Player
from models.scout import Scout
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.user import User
from models.position import Position

db = "sqlite:///footDB.db"
engine = create_engine(db, pool_pre_ping=True)
session = Session(engine)

all_clubs = session.query(Club).all()
club_ids = [club.id for club in all_clubs]
for club_id in club_ids:
    club = session.query(Club).filter(Club.id == club_id).first()
    for i in range(4):  # create 4 players for each club
        player = Player(
            email=f"player{i}@{club.name}.com",
            password="password",
            first_name=f"Player{i}",
            last_name=f"{club.name}",
            height=180,
            weight=75,
            club_id=club.id,
            date_of_birth=datetime.datetime.utcnow()
        )
        session.add(player)
        scout = Scout(
            email=f"scout{i}@{club.name}.com",
            password="password",
            first_name=f"Scout{i}",
            last_name=f"{club.name}",
            club_id=club.id
        )
        session.add(scout)


all_users = session.query(User).all()
all_players = session.query(Player).all()
for player in all_players:
    post = Post(
        content=f"Content by {player.first_name} {player.last_name}",
        player_id=player.id
    )
    session.add(post)

all_scouts = session.query(Scout).all()
for scout in all_scouts:
    post = Post(
        content=f"Content by {scout.first_name} {scout.last_name}",
        scout_id=scout.id
    )
    session.add(post)

all_posts = session.query(Post).all()
for post in all_posts:
    for player in all_players:
        if post.player_id != player.id:
            comment_p = Comment(
                text=f"Comment by {player.first_name} {player.last_name}",
                post_id=post.id,
                player_id=player.id
            )
            session.add(comment_p)
            like_p = Like(
                post_id=post.id,
                player_id=player.id
            )
            session.add(like_p)
    for scout in all_scouts:
        if post.scout_id != scout.id:
            comment_s = Comment(
                text=f"Comment by {scout.first_name} {scout.last_name}",
                post_id=post.id,
                scout_id=scout.id
            )
            session.add(comment_s)
            like_s = Like(
                post_id=post.id,
                scout_id=scout.id
            )
            session.add(like_s)
    for user in all_users:
        comment_u = Comment(
            text=f"Comment by {user.first_name} {user.last_name}",
            post_id=post.id,
            user_id=user.id
        )
        session.add(comment_u)
        like_u = Like(
            post_id=post.id,
            user_id=user.id
        )
        session.add(like_u)

session.commit()

all_positions = session.query(Position).all()
for player in all_players:
    positions_for_player = random.sample(all_positions, 3)
    for position in positions_for_player:
        player.positions.append(position)
    session.commit()

    scouts_for_player = random.sample(all_scouts, 5)
    for scout in scouts_for_player:
        player.scouts.append(scout)
    session.commit()

session.commit()
session.close()
