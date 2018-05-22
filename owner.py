from flask import Flask, Blueprint, render_template
import boto3
from s3_run import *


app = Flask(__name__)
Bootstrap(app)
owner_port= Blueprint('owner_port',__name__)

@owner_port.route('/delete_owner',methods=['GET','POST'])
def delete_owner():
    if request.method=='POST':
        the_owner=request.form.get('delete_id')
        return '<h1>The owner list valid is</h1>'+str(the_owner)


@owner_port.route('/add_owner',methods=['GET','POST'])
def add_owner():
    if request.method=='POST':
        the_owner=request.form.get('owner_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nric = request.form.get('nric')
        email = request.form.get('email')
        occupation = request.form.get('occupation')
        bank_balance = request.form.get('bank_balance')
        ccris = request.form.get('ccris')
        ctos = request.form.get('ctos')
        return '<h1>The owner list valid is</h1>'+str(the_owner)


@owner_port.route('/owner',methods=['GET','POST'])
def owner_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table1 = dynamodb.Table('owner')
    response1 = table1.scan()
    response_1 = response1['Items']
    return render_template('table_owner.html',data=response_1)

