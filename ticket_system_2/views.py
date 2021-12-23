from os import name
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Ticket, Notification, Asset, User, Comment
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

# accessing the home page 
@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    else:
        return render_template("home.html", user=current_user, first_name=current_user.first_name)

@views.route('/create-asset', methods=['POST', 'GET'])
@login_required
def create_asset():
    # if request is a post request and the following fields are satisfied then the asset will be created in the database.
    if request.method == 'POST':
        asset_tag = request.form.get('asset-tag-content')
        serial_num = request.form.get('serial-number-content')
        asset_type = request.form.get('asset-type-content')
        asset_maker = request.form.get('asset-maker-content')
        # filtering the asset table asset tag and then querying the database
        asset = Asset.query.filter_by(asset_tag=asset_tag).first()
        # checking if all fields are not empty, if a field is empty flashed message will appear 
        if serial_num == '' or asset_tag == '' or asset_type == '' or asset_maker == '':
            flash('No field can be empty.', category='error')
        else:
            # checking if the asset tag entered equlas another asset tag in the database (Asset table)
            if asset: 
                flash('Asset already exists.', category='error')
                return redirect(url_for("views.create_asset"))
            # checking if the asset tag entered has 14 characters     
            elif len(asset_tag) != 14:
                flash('Asset tag must be 14 characters.', category='error')
                return redirect(url_for("views.create_asset"))
            # checking if the serial number entered has 10 characters
            elif len(serial_num) != 10:
                flash('Serial number must be 10 characters.', category='error')
                return redirect(url_for("views.create_asset"))
            # adding the new asset after going through the checks  
            else:
                new_asset = Asset(asset_tag=asset_tag, serial_num=serial_num, asset_type=asset_type, asset_maker=asset_maker, creator=current_user.email)
                db.session.add(new_asset) 
                db.session.commit() 
                flash('Asset has been added!', category='success')
                return redirect(url_for("views.assets"))
    else:
        return render_template("create_asset.html", user=current_user)

# page for each individual asset
@views.route('/assets/<asset_tag>', methods=['POST', 'GET'])
@login_required
def asset_page(asset_tag):
    if request.method == 'POST':
        pass
    else:
        # getting the asset from the asset table in the database that matches the asset tag passed in the parameter
        # getting all the tickets that match the asset tag passed in the parameter
        asset = Asset.query.filter_by(asset_tag=asset_tag).first()
        tickets = Ticket.query.filter_by(asset_tag=asset_tag).all()

        if not asset:
            flash('Asset does not exist.', category='error')
            return redirect(url_for('views.assets'))
        
        else:
            # calling asset and ticket to display the info from the database
            return render_template("asset_page.html", user=current_user, asset=asset, tickets=tickets)
           

@views.route('/assets', methods=['POST', 'GET'])
@login_required
def assets():
    if request.method == 'POST':
        pass
    else:
        # displaying all assets in the database from the Asset table
        assets = Asset.query.all()    
        return render_template("assets.html", user=current_user, assets=assets)

@views.route('/create-ticket', methods=['POST', 'GET'])
@login_required
def create_ticket():
    # if request is a post request and the following fields are satisfied then the ticket will be created in the database.
    if request.method == 'POST':
        asset_tag = request.form.get('asset-tag-ticket-content')
        issue = request.form.get('issue-content')
        # filtering the asset table asset tag and then querying the database
        asset = Asset.query.filter_by(asset_tag=asset_tag).first()
        # checking if the asset_tag field and issue fields are satisfied.
        if asset_tag == '' or issue == '':
            flash('No fields can be empty.', category='error')
            return redirect(url_for('views.create_ticket'))
        else:
            # checking the length of the asset tag
            if len(asset_tag) != 14:
                flash('Asset tag must have 14 characters.', category='error')
                return redirect(url_for('views.create_ticket'))
            else:
                # checking if the asset tag is equal to another asset tag from asset table in the database
                if asset:
                    # creating the ticket with class objects(asset_tag, issue, and current_user.id) passed to it if checks are passed
                    new_ticket = Ticket(asset_tag=asset_tag, issue=issue, author=current_user.email)
                    db.session.add(new_ticket)
                    db.session.commit()
                    flash('Ticket has been submitted!', category='success')
                    return redirect(url_for("views.tickets"))
                else:
                    flash('Cannot find that asset. Make sure asset tag is entered correctly.', category='error')
                    return redirect(url_for('views.create_ticket'))
    else:
        return render_template("create_ticket.html", user=current_user)

# page for each individual ticket 
@views.route('/tickets/<id>', methods=['POST', 'GET'])
@login_required
def ticket_page(id):
    if request.method == 'POST':
        pass
    else:
        # getting the ticket with the id passed in the parameter from the ticket table in the database
        ticket = Ticket.query.filter_by(id=id).first()
        comments= Comment.query.filter_by(ticket_id=id).all()
        # if the ticket doesn't exist redirecting user to tickets page 
        if not ticket: 
            flash('Ticket does not exist.', category='error')
            return redirect(url_for('views.tickets'))
        
        return render_template("ticket_page.html", user=current_user, ticket=ticket, comments=comments)
    

@views.route('/create-comment/ticket/<ticket_id>', methods=['POST'])
@login_required
def create_comment(ticket_id):
    # getting the content entered by the user (which is the comment)
    content = request.form.get('text')

    if not content:
        # if user presses add comment button with adding comment, flashed message will appear and user will be redirected to the ticket_page
        flash('Comment cannot be empty.', category='error')
        return redirect(url_for('views.ticket_page', id=ticket_id))
    else:
        # otherwise, filtering the tickets by id and then getting comment if the ticket is found.
        ticket = Ticket.query.filter_by(id=ticket_id)
        if ticket:
            comment = Comment(content=content, author=current_user.email, ticket_id=ticket_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Ticket does not exist.', category='error')
            return redirect(url_for('views.tickets'))

    

    return redirect(url_for('views.ticket_page', id=ticket_id))

@views.route('/tickets', methods=['POST', 'GET'])
@login_required
def tickets():
    if request.method == 'POST':
        pass
    else:
        # displaying all tickets in the database from the Ticket table
        tickets = Ticket.query.all()    
        return render_template("tickets.html", user=current_user, tickets=tickets)

@views.route('/notifications', methods=['POST', 'GET'])
@login_required
def notifications():
    if request.method == 'POST':
        pass
    else:
        return render_template("notifications.html", user=current_user)

@views.route('/help')
@login_required
def help():

    return render_template("help.html", user=current_user)

@views.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        pass
    else:
        return render_template("profile.html", user=current_user)

@views.route('/profile-settings', methods=['POST', 'GET'])
@login_required
def profile_settings():
    if request.method == 'POST':
        pass
    else:
        return render_template("profile_settings.html", user=current_user)

