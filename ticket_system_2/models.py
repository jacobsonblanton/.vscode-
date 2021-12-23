from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash


from . import db
from sqlalchemy.sql import func


# creating the User class and object. Declaring what will be stored under User in the database. 
# creating User relationships with the 'ticket', 'notification', and 'asset'
# this relationship is defined as the user can have one-to-many relationship with these class objects (User-having many-tickets, User-having many-
#  assets, User-having many- notifications)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    tickets = db.relationship('Ticket', backref='user')
    # notifications = db.relationship('Notification', backref='user', passive_deletes=True)
    assets = db.relationship('Asset', backref='user')
    comments = db.relationship('Comment', backref='user')

# creating a Ticket class and object to reference in the database
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asset_tag = db.Column(db.String(20), nullable=False)
    issue = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='ticket')

    
# creating an Asset class and object to reference in the database 
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(20), nullable=False)
    serial_num = db.Column(db.String(20), nullable=False)
    asset_type = db.Column(db.String(20), nullable=False)
    asset_maker = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# creating a Notification class and object to reference in the database
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    # asset_id = db.Column(db.Integer, db.ForeignKey('asset.id', ondelete="CASCADE"), nullable=False)
    # ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', ondelete="CASCADE"), nullable=False)

# creating a Comment class to leave on tickets 
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
