from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import boto3

app = Flask(__name__)
Bootstrap(app)
claim = Blueprint('claim',__name__)
pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"

@claim.route('/company_claim',methods=['POST','GET'])
def company_claim():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table1 = dynamodb.Table('company_claim')
    table2 = dynamodb.Table('claim_company_expenses')
    response1 = table1.scan()
    response_1 = response1['Items']
    response2 = table2.scan()
    response_2 = response2['Items']
    return render_template('company_claim.html',data=response_1,transactions=response_2,pdf_reader=pdf_reader_link)

@claim.route('/register_company',methods=['POST','GET'])
def register_claim_company():
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
        table = dynamodb.Table('company_claim')
        global employee_claim_id, company_id, claim_person_id, claim_limit
        employee_claim_id=request.form.get('employee_claim_id')
        company_id = "company18"
        claim_person_id= request.form.get('claim_person_id')
        claim_limit = request.form.get('claim_limit')#company18 - Exxon Mobile
        table.put_item(
            Item={
                'employee_claimID': employee_claim_id,
                'companyID': company_id,
                'ownerID': claim_person_id,
                'from_companyID': company_id,
                'claim_limit': int(claim_limit),
            })
        return company_claim()



