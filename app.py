from flask import Flask, render_template, request, make_response, url_for
from flask_mail import Mail, Message
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)  # ✅ This is what Gunicorn needs!

# Then your routes follow...
@app.route('/')
def index():
    return render_template('index.html')

