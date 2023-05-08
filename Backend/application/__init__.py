from flask import Flask
from flask_cors import CORS

app=Flask(__name__)
# CORS(app, supports_credentials=True)
app.secret_key="otp"
CORS(app)

from application import views 