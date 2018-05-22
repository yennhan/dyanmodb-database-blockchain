from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
import requests
from s3_run import *



app = Flask(__name__)
Bootstrap(app)
land= Blueprint('land_title',__name__)


@land.route('/land_title',methods=['GET','POST'])
def land_title():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('land_title')
    response = table.scan()
    response_1 = response['Items']
    return render_template('land_title.html',data=response_1)

@land.route('/add_land',methods=['GET','POST'])
def add_land():
    if request.method=='POST':
        the_owner = request.form.get('owner_id')
        land_id = request.form.get('land_id')
        lot_no = request.form.get('lot_no')
        size_meter = request.form.get('size_meter')
        lembaran_piawai = request.form.get('lembaran_piawai')
        negeri = request.form.get('negeri')
        daerah = request.form.get('daerah')
        location_type = request.form.get('location')
        tanah = request.form.get('tanah')
        return land_title()