#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint,boto3

app = Flask(__name__)
Bootstrap(app)

company= Blueprint('company',__name__)




@company.route('/company_homepage',methods=['GET','POST'])
def company_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('company')
    response=table.scan()
    response_1=response['Items']
    return render_template('company_dashboard.html',data=response_1)

@company.route('/add_company',methods=['GET','POST'])
def add_company():
    if request.method == 'POST':
        the_company_name= request.form.get('company_name')
        company_category=request.form.get('company_category')
        employee_id = request.form.get('employee_id')

        dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
        table = dynamodb.Table('company')
        response = table.scan()
        response_1 = response['Items']
        table.put_item(
            Item={
                'companyID': "company"+str(len(response_1)),
                'company_name':the_company_name,
                'employee_in_this_company_ID':[employee_id],
                'company_category':[company_category]
            }
        )
        return company_homepage()
@company.route('/delete_company',methods=['GET','POST'])
def delete_company():
    if request.method=='POST':
        the_firm = request.form.get('company_ID')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return '<h1>The owner list valid is</h1>'+str(the_list)
