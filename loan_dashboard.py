#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import boto3

app = Flask(__name__)
Bootstrap(app)


loan= Blueprint('loan',__name__)
'''
{
    "$class": "org.acme.model.LoanAgreement",
    "loan_id": "loan_owner3",
    "owner": "resource:org.acme.model.owner#owner3",
    "bank": "resource:org.acme.model.Bank#bank2",
    "the_approval": "Yes",
    "loan_term": 30,
    "loan_amount": 30000,
    "interest_rate": 4.5,
    "blr_rate": 4,
    "lock_in_period_in_year": 5,
    "penalty": 0,
    "rgbt": ".",
    "flexi_loan": "YES"
}
'''

@loan.route('/loan_agreement_dashboard',methods=['GET','POST'])
def loan_dashboard():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('loan_agreement')
    response = table.scan()
    response_1 = response['Items']
    return render_template('loan_agreement.html', data=response_1)