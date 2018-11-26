from flask import Flask, request, jsonify, current_app
from application.extensions import db


class Public(db.Model, CRUDMixin):
    id = db.Column(db.String(), primary_key=True, nullable=False)
    value = db.Column(db.JSON())
