from flask import Flask, request
import os
import main
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def call_main():
    return main.send_messages(request)