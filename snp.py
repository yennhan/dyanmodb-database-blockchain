from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint

app = Flask(__name__)
Bootstrap(app)


pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"


#register the blueprint
snp= Blueprint('snp',__name__)


@snp.route('/snp')
def transactions():
    return render_template('snp.html')

