"""
Routes for handling the home page and related functionalities.

This module includes routes for rendering the home page and clearing entry approvals.
It also includes role-based rendering of the home page based on the 'role' query parameter.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import EntryApproval, LoginLogout
from .. import DB, logging
from .admin import superuser_required

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Renders 'system.html' based on the user's role.

    GET:
        Retrieves the 'role' query parameter to determine the user's role.
        Logs user access to the home route.
        Renders 'system.html' with current user information based on their role.
    """
    role = request.args.get('role')
    logging.info(f"User '{current_user.username}' accessed the home route")
    return render_template("system.html", user=current_user)
 

@home_routes.route('/clear_entry_approvals')
@login_required
@superuser_required
def clear_entry_approvals():
    """
    Clears all entry approvals.

    GET:
        Deletes all records from the 'LoginLogout' table (EntryApproval).
        Commits the changes to the database.
        Logs the number of deleted entry approvals and user action.
        Flashes a success message.
        Redirects back to the home page.
    """
    try:
        num_deleted = LoginLogout.query.delete()  
        DB.session.commit()
        logging.info(f"Cleared {num_deleted} entry approvals (by: {current_user.username})")
        flash("Cleared")

    except Exception as e:
        logging.error(f"Failed to clear entry approvals: {e}")
        flash("Failed to clear peak hours." , 'error') 

    return redirect(url_for('home_routes.home'))
    
if __name__ == '__main__':
    None