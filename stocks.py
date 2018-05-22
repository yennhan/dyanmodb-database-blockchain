from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint
from receipt_generator import *
from smart_contract_case_study_2 import *
from supplier2 import *
from supplier1 import *
app = Flask(__name__)
Bootstrap(app)
stocks = Blueprint('stocks',__name__)


pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"


@stocks.route('/home_stocks',methods=['GET','POST'])
def stock_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    get_expenses = dynamodb.Table('stock')
    the_list = get_expenses.scan()
    the_list = the_list['Items']
    data_invoice = []
    get_restock = dynamodb.Table('request_stock')
    the_restock = get_restock.scan()
    the_restock = the_restock['Items']
    for i in range(len(the_restock)):
        if the_restock[i]['restock_status'] == "Required_restock":
            data_invoice.append(the_restock[i])
    receipt_first = dynamodb.Table('receipt')
    the_receipt_id = receipt_first.scan()
    the_receipt_id = the_receipt_id['Items']
    data_receipt=[]
    for i in range(len(the_receipt_id)):
        word=(the_receipt_id[i]['receiptID'].split("b",1))
        if word[0]=="stock_receipt":
            data_receipt.append(the_receipt_id[i])
    return render_template('stocks.html',data=the_list,restock=data_invoice,pdf_reader=pdf_reader_link,receipts=data_receipt)

@stocks.route('/add_stocks',methods=['GET','POST'])
def add_stock():
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
        item_name=request.form.get('item_name')
        item_balance=request.form.get('stock_balance')
        item_standard=request.form.get('standard_level')
        item_price_per_unit=request.form.get('price_per_unit')
        company_name="company13"
        get_expenses = dynamodb.Table('stock')
        the_list = get_expenses.scan()
        get_expenses.put_item(
            Item={
                'stockID': "stock_"+str(len(the_list)+1)+"_company13",
                'companyID': company_name,
                'item_name': item_name,
                'stock_balance': item_balance,
                'standard_level':item_standard,
                'price_per_unit':item_price_per_unit
            })
        return stock_homepage()

@stocks.route('/purchase_confirm',methods=['GET','POST'])
def purchase_stock():
    if request.method == 'POST':
        stock_id= request.form.get('stockid')
        supplier_id = request.form.get('supplier_id')
        requeststock_id= request.form.get('requeststock_id')
        if supplier_id=="supplier2":
            purchased_supplier2(stock_id,requeststock_id)
        else:
            purchased_supplier1(stock_id,requeststock_id)
    return redirect(url_for('stocks.stock_homepage'))

@stocks.route('/delete_stocks',methods=['GET','POST'])
def delete_stock():
    if request.method == 'POST':
        #item_id = request.form.get('delete_id')
        #headers = {'Content-type': 'application/json'}
        #claim_post = stock_url +'/'+item_id+ token
        #response = requests.delete(claim_post,headers=headers)
        return stock_homepage()

@stocks.route('/bidding_request',methods=['GET','POST'])
def bid_request():
    if request.method == 'POST':
        item_id=request.form.get("bid_id")
        print(item_id)
        return stock_homepage()
