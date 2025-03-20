"""
https://flask.palletsprojects.com/en/stable/
Flask: https://readthedocs.org/projects/flask-restful/downloads/pdf/latest/
Flask-RESTful Documentation, Release 0.3.10
"""

# Infrastructure
import sys
import os
from os import environ

from flask import Flask
from flask_restx import Api

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Application
from resources.version import VersionInfo
from resources.finance_data import TickerInfo, TickerData, IntrinsicValue, IntrinsicValues


# Flask application
app = Flask(__name__)
api = Api(app)

# Register Endpoints
api.namespace('YFinanceService', description='YFinance Service API')

api.add_resource(VersionInfo, '/YFinanceService/VersionInfo')
api.add_resource(TickerInfo, '/YFinanceService/TickerInfo')
api.add_resource(TickerData, '/YFinanceService/TickerData')
api.add_resource(IntrinsicValue, '/YFinanceService/IntrinsicValue')
api.add_resource(IntrinsicValues, '/YFinanceService/IntrinsicValues')


if __name__ == '__main__':
    DEBUG = False
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    # run our Flask app
    app.run(HOST, PORT, DEBUG)
