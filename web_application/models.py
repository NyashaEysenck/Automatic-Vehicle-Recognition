"""
Defines database models for the application using SQLAlchemy.

Dependencies:
- DB: SQLAlchemy database instance.
- UserMixin: Provides default implementations for the methods that Flask-Login expects a user object to have.
- func: Provides functions used in SQL expressions.

Models:
- Client: Represents a client in the system with their details and associated vehicles and entry approvals.
- Vehicle: Represents a vehicle associated with a client.
- EntryApproval: Represents an approval record for a client's vehicle entry.
- LoginLogout: Represents a log of client entries and exits.
- Guard: Represents a guard user with login credentials and associated logs.
"""
from . import DB
from flask_login import UserMixin
from sqlalchemy.sql import func

class Client(DB.Model):
    client_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    first_name = DB.Column(DB.String(255), nullable=False)
    last_name = DB.Column(DB.String(255), nullable=False)
    address = DB.Column(DB.String(255), nullable=False)
    phone_number = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False, unique = True)
    vehicles = DB.relationship('Vehicle', backref='client', lazy='dynamic')
    entry_approvals = DB.relationship('EntryApproval', backref='client', lazy=True)

    def get_id(self):
        return str(self.client_id)

class Vehicle(DB.Model):
    vehicle_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    client_id = DB.Column(DB.Integer, DB.ForeignKey('client.client_id'), nullable=False)
    plate_num = DB.Column(DB.String(255), nullable=False, unique = True)
    owners_name = DB.Column(DB.String(255), nullable=False)
    make = DB.Column(DB.String(255), nullable=False)
    model = DB.Column(DB.String(255), nullable=False)
    color = DB.Column(DB.String(255), nullable=False)

    def get_id(self):
        return str(self.vehicle_id)

class EntryApproval(DB.Model):
    approval_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    client_id = DB.Column(DB.Integer, DB.ForeignKey('client.client_id'), nullable=True)
    guard_id = DB.Column(DB.Integer, DB.ForeignKey('guard.guard_id'), nullable=True)
    approval_status = DB.Column(DB.Boolean, nullable=False)
    approval_time = DB.Column(DB.DateTime, nullable=False)

    def get_id(self):
        return str(self.approval_id)

    @property
    def status(self):
        return "Approved" if self.approval_status else "Denied"
    
class LoginLogout(DB.Model):
    entry_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    guard_id = DB.Column(DB.Integer, DB.ForeignKey('guard.guard_id'), nullable=True)
    client_id = DB.Column(DB.Integer, DB.ForeignKey('client.client_id'), nullable=False)
    login_time = DB.Column(DB.DateTime, nullable=False)
    logout_time = DB.Column(DB.DateTime, nullable=True)
    plate_num = DB.Column(DB.String(255), nullable=False, unique = False)
    

    def get_id(self):
        return str(self.entry_id)


class Guard(DB.Model, UserMixin):
    guard_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    username = DB.Column(DB.String(255), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False, unique=True)
    entry_logs = DB.relationship('LoginLogout', backref='guard', lazy=True)
    supervisor = DB.Column(DB.Boolean, nullable=False)
    suspended = DB.Column(DB.Boolean, nullable=False)

    def get_id(self):
        return str(self.guard_id)