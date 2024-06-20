"""
Password reset routes for the Flask web application.

This module provides routes and functionalities for resetting passwords
for user accounts. It includes generating password reset tokens, sending
reset instructions via email, and handling password reset forms.

Modules:
    flask: Provides the core components for Flask web application framework.
    flask_mail: Provides email functionalities for Flask.
    flask_login: Provides user session management for Flask.
    werkzeug.security: Provides utilities for password hashing.
    ..models: Contains the application's database models.
    ..: Provides the token serializer, mail instance, database instance, and logging.

Functions:
    forgot_password: Handles the initiation of the password reset process.
    reset_password: Handles resetting the password based on the provided token.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import Guard
from .. import SERIALIZER, MAIL, DB, logging
from flask_mail import Message
from flask_login import current_user
from werkzeug.security import generate_password_hash

# Create a Blueprint for the password reset feature
forgot = Blueprint('forgot', __name__)

@forgot.route('/forgot_password<email>', methods=['GET', 'POST'])
def forgot_password(email):
    """
    Initiates the password reset process.

    Args:
        email (str): The email address of the user requesting the password reset.

    Returns:
        Redirects to the password reset link if the user is a supervisor.
        Sends an email with password reset instructions and redirects to the login page on success.
        Renders the forgot_password form on GET request or when form submission fails.
    """
    if email == "None":
        email = None
   
    if current_user.supervisor and email:
        # Generate a password reset token
        token = SERIALIZER.dumps(email, salt='password-reset') 
        # Create a full URL for the password reset page (including the token)
        reset_link = url_for('forgot.reset_password', token=token, _external=True)
        
        return redirect(reset_link)
            
    # Handle form submission (POST request)
    if request.method == 'POST':
        email = request.form['email']
        user = Guard.query.filter_by(email=email).first()

        # If a user with the provided email is found:
        if user:
            # Generate a password reset token
            token = SERIALIZER.dumps(current_user.email, salt='password-reset') 
            # Create a full URL for the password reset page (including the token)
            reset_link = url_for('forgot.reset_password', token=token, _external=True)

            # Construct the password reset email
            msg = Message('Password Reset Request',
                          recipients=[email])
           
            msg.body = f'To reset your password, visit the following link: {reset_link} \nIf you did not request this, please ignore this email.'
            try:

                # Send the password reset email
                MAIL.send(msg)
                # Display a success message and redirect to the login page
                flash('Password reset instructions sent! Check your email.', 'success')
                logging.info(f"Password reset email sent to: {email}")

            except Exception as e:
                logging.error(f"Failed to send password reset email to {email}: {e}")
                flash("Try again" , (str(e)))
                return redirect(url_for('forgot.forgot_password'))

            # Display a success message and redirect to the login page
            flash('Password reset instructions sent! Check your email.', 'success')
            return redirect(url_for('auth.login'))  
        else:
            # If the user is not found, display an appropriate message
            logging.info(f"Password reset requested for non-existent email: {email}")            
            flash('No account found with that email.', 'error') 

    # Display the forgot password form (GET request or if POST failed)
    return render_template('forgot_password.html', user=current_user) 

@forgot.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Handles resetting the user's password based on the provided token.

    Args:
        token (str): The password reset token received via email.

    Returns:
        Updates the user's password and redirects to the login page on success.
        Renders the reset_password form on GET request or when form submission fails.
    """
    # Attempt to decode the token
    try:
        email = SERIALIZER.loads(token, salt='password-reset', max_age=3600)  # Ensure token validity and set a 1-hour expiration
    except:
        # Handle invalid or expired tokens
        logging.warning("Invalid or expired password reset token.")  # Log Security Warning
        flash('Invalid or expired password reset link.', 'error')
        return redirect(url_for('auth.login'))  
    
    # Handle password reset form submission (POST request)
    if request.method == 'POST':
        new_password = request.form['password']
        user = Guard.query.filter_by(email=email).first()

        # Update the user's password  
        user.password = generate_password_hash(new_password , method='scrypt', salt_length=16)
        DB.session.commit()  
        flash(f"Password reset successful for user: {email}")

        logging.info(f"Password reset successful for user: {email}")

       # Display a success message and redirect to login
        flash('Your password has been updated. Please log in.', 'success')
        return redirect(url_for('auth.login'))
 

    # Display the password reset form (GET request)
    return render_template('reset_password.html', token=token, user=current_user)

if __name__ == '__main__':
    None