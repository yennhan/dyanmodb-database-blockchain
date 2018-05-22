from flask import *
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint,boto3
from receipt_generator import *
from smart_contract_case_study_2 import *
from invoice_generator import *
from stocks import *
app = Flask(__name__)
Bootstrap(app)
supplier3 = Blueprint('supplier3',__name__)



pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"


#veggy supplier
@supplier3.route('/supplier1_homepage',methods=['GET','POST'])
def supplier_homepage():
    data_invoice = []
    things=[]
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('request_stock')
    get_restock = request_stock.scan()
    the_restock = get_restock['Items']
    for i in range(len(the_restock)):
        if the_restock[i]['supplierID'] == "supplier3" and the_restock[i]['restock_status'] == "Required_restock":
            data_invoice.append(the_restock[i])
    for i in range(len(the_restock)):
        if the_restock[i]['supplierID']=="supplier3" and the_restock[i]['restock_status']=="Completed":
            things.append(the_restock[i])
    return render_template('supplier3_dashboard.html', invoice=data_invoice,data=things)


@supplier3.route('/adding_invoice_supplier1',methods=['GET','POST'])
def adding_invoice_supplier1():
    data_invoice=[]
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('request_stock')
    get_restock = request_stock.scan()
    the_restock = get_restock['Items']
    return supplier_homepage()


@supplier3.route('/purchased',methods=['GET','POST'])
def purchased_supplier1(stock_id,request_stock_id):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('stock')
    response1 = request_stock.get_item(
        Key={
            'stockID': stock_id
        })
    standard = response1['Item']

    request_stock.update_item(
        Key={
        'stockID':stock_id
    },
        UpdateExpression = "set stock_balance = :r",
        ExpressionAttributeValues = {
                ':r': int(standard['standard_level']*2)
                },
        ReturnValues = "UPDATED_NEW"
    )
    item = {}
    item['qty'] = int((standard['standard_level'] * 2))
    item['description_of_item'] = standard['item_name']
    item['unit_price'] = float(standard['price_per_unit'])
    item['amount'] = int(item['qty'] * item['unit_price'])
    request_stock_1 = dynamodb.Table('request_stock')
    response2 = request_stock_1.update_item(
        Key={
            'requeststockID': request_stock_id
        },
        UpdateExpression="set restock_status = :r",
        ExpressionAttributeValues={
            ':r': "Completed"
        },
        ReturnValues="UPDATED_NEW"
    )
    logo_im = 'lucky_frozen.png'
    company_name = "Lucky Frozen"
    company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
    purchaser = "Jibby & Co"
    account_id = ""
    company_claim = ""
    the_data = []
    the_data.append(item)
    time1 = time.asctime(time.localtime(time.time()))
    receipt_first = dynamodb.Table('receipt')
    the_receipt_id = receipt_first.scan()
    the_receipt_id = the_receipt_id['Items']
    receipt_id = "stock_receiptb_" + str(len(the_receipt_id))
    receipt = {}
    receipt['receiptID'] = receipt_id
    receipt['total_price'] = item['amount']
    receipt['companyID'] = "company20"
    receipt['total_cost'] = 0
    dumb_data_to_receipt_asset(receipt)
    a = receipt_id.split("b", 1)
    receipt_pdf_generator(logo_im, receipt_id, company_name, company_address, purchaser, time1, the_data, account_id,company_claim)
    s3_setup(receipt_id + ".pdf")
    silentremove(receipt_id + ".pdf")

def dumb_data_to_receipt_asset(data):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    receipt1 = dynamodb.Table('receipt')
    receipt1.put_item(
        Item={
            'receiptID': data['receiptID'],
            'total_price': data['total_price'],
            'companyID': data['companyID'],
            'total_cost': data['total_cost']
        })


@supplier3.route('/issue_invoice',methods=['GET','POST'])
def issue_invoice():
    if request.method == 'POST':
        invoice_id = request.form.get('issue_invoice')
        restock_id = request.form.get('request_stock_id')
        dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
        stock = dynamodb.Table('stock')
        response=stock.get_item(
            Key={
                'stockID':invoice_id
            }
        )
        the_list=response['Item']
        invoice_id = "invoice_" + restock_id
        company_name = "Lucky Frozen"
        company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
        purchaser = "Jibby & Co"
        time1 = time.asctime(time.localtime(time.time()))
        the_items = []
        data = {}
        data['qty'] =(int((the_list['stock_balance'])*2))
        data['description_of_item'] = the_list['item_name']
        data['unit_price'] = float(the_list['price_per_unit'])
        print(data['qty'])
        print(data['unit_price'])
        data['amount'] = int((data['qty'] * data['unit_price']))
        the_items.append(data)
        logo_im = 'lucky_frozen.png'
        invoice_pdf_generator(logo_im, invoice_id, company_name, company_address, purchaser, time1, the_items)
        s3_setup(invoice_id + ".pdf")
        silentremove(invoice_id + ".pdf")
        return adding_invoice_supplier1()

@supplier3.route('/submit_bidding',methods=['GET','POST'])
def submit_bidding():
    return supplier_homepage()
