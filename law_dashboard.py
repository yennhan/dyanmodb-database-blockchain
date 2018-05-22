#Leow Yenn Han
#leowyennhan@gmail.com

from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, boto3


app = Flask(__name__)
Bootstrap(app)

law_dashboard= Blueprint('law',__name__)

"""
"$class": "org.acme.model.Lawyer",
    "lawfirmID": "lawfirm0",
    "lawyer_firm_id": "resource:org.acme.model.company#company20",
    "lawyer_id": "Rahayu_Partnership_lawyer_0",
    "company_lawyer_name": "Rahayu_Partnership"
"""

@law_dashboard.route('/law_homepage',methods=['GET','POST'])
def law_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('lawyer')
    response = table.scan()
    response_1 = response['Items']
    return render_template('law_dashboard.html',data=response_1)

@law_dashboard.route('/law_add_firm',methods=['GET','POST'])
def law_add_firm():
    if request.method == 'POST':
        the_firm = request.form.get('delete_id')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return law_homepage()

@law_dashboard.route('/delete_firm',methods=['GET','POST'])
def delete_firm():
    if request.method=='POST':
        the_firm = request.form.get('lawfirm_id')
        get_firm = requests.get(the_firm)
        the_list = get_firm.json()
        return law_homepage()

