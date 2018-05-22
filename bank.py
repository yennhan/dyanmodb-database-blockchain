#Leow Yenn Han
#leowyennhan@gmail.com
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import boto3


app = Flask(__name__)
Bootstrap(app)

banks= Blueprint('banks',__name__)



@banks.route('/bank_homepage',methods=['GET','POST'])
def bank_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('bank')
    response = table.scan()
    response1=response['Items']
    return render_template('bank.html',data=response1)
