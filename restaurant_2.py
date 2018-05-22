from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint,boto3
from receipt_generator import *
from smart_contract_case_study_2 import *
from profit_loss_pdf import *
app = Flask(__name__)
Bootstrap(app)
restaurant2 = Blueprint('restaurant2',__name__)


pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"

#add receipt and claims
@restaurant2.route('/restaurant_2',methods=['GET','POST'])
def home_page():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    receipt = dynamodb.Table('receipt')
    the_receipt1 = receipt.scan()
    the_receipt1 = the_receipt1['Items']
    data_receipt=[]
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] != "stock_receipt":
            data_receipt.append(the_receipt1[i])
    pdf_name="jibbyco.pdf"
    company_name="Jibby&Co"
    company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
    #get receipt revenue
    revenue=0
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] != "stock_receipt":
            revenue+=int(the_receipt1[i]['total_price'])
    cost_of_goods=0
    for i in range(len(the_receipt1)):
        word = (the_receipt1[i]['receiptID'].split("b", 1))
        if word[0] == "stock_receipt":
            cost_of_goods+=int(the_receipt1[i]['total_price'])
    total_salary = 10000
    rental = 5000
    office_supply = 100
    insurance = 3000
    utilities = 1500
    maintanence = 700
    telecommunication = 300
    profit_loss_pdf(pdf_name,company_name, company_address, revenue, cost_of_goods, total_salary, rental, office_supply,insurance, utilities, maintanence, telecommunication)
    s3_setup(pdf_name)
    silentremove(pdf_name)
    return render_template('restaurant_2.html', restaurant_data=data_receipt, pdf_reader=pdf_reader_link,pl_statement=pdf_name)


@restaurant2.route('/restaurant2_claim',methods=['GET','POST'])
def the_one_claiming():
    if request.method == 'POST':
        chick_breakie = request.form.get('chick_breakie')
        jibby_big_breakfast= request.form.get("big_breakfast")
        casa_egg = request.form.get("casablanca_egg")
        trio_drips=request.form.get('trio_drips')
        para_break=request.form.get("paradise_breakie")
        cala_salad=request.form.get("calamari_salad")
        rib_eye=request.form.get("rib_eye_steak")
        beef_ribs=request.form.get("sticky_bbq_beef_ribs")
        salmon_russian=request.form.get("salmon_russian")
        calculate_cost(chick_breakie,jibby_big_breakfast,casa_egg,trio_drips,para_break,cala_salad,rib_eye,beef_ribs,salmon_russian)
        return home_page()
    return home_page()