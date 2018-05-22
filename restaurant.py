
from s3_run import *
import boto3
from receipt_generator import *
app = Flask(__name__)
Bootstrap(app)
restaurant = Blueprint('restaurant',__name__)


pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"

#add receipt and claims
@restaurant.route('/restaurant_one',methods=['GET','POST'])
def the_one_claiming():
    item=[]
    data={}
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
        if chick_breakie!='':
            data["qty"]=int(chick_breakie)
            data["unit_price"]=30
            data['description_of_item']="Chick Breakie"
            data['amount']= 30*int(chick_breakie)
            item.append(data)
            data={}
        if jibby_big_breakfast!="":
            data["qty"]=int(jibby_big_breakfast)
            data["unit_price"]=31
            data['description_of_item']="Jibby Big Breakfast"
            data['amount']=31*int(jibby_big_breakfast)
            item.append(data)
            data = {}
        if casa_egg!="":
            data["qty"] = int(casa_egg)
            data["unit_price"] = 28
            data['description_of_item'] = "Casabalanca Egg"
            data['amount'] = 28 * int(casa_egg)
            item.append(data)
            data = {}
        if trio_drips!="":
            data["qty"] = int(trio_drips)
            data["unit_price"] = 22
            data['description_of_item'] = "Jibby Trio Drips"
            data['amount'] = 22 * int(trio_drips)
            item.append(data)
            data = {}
        if para_break != "":
            data["qty"] = int(para_break)
            data["unit_price"] = 25
            data['description_of_item'] = "Paradise Breakie"
            data['amount'] = 25 * int(para_break)
            item.append(data)
            data = {}
        if cala_salad != "":
            data["qty"] = int(cala_salad)
            data["unit_price"] = 22
            data['description_of_item'] = "Crispy Calamari Salad"
            data['amount'] = 22 * int(cala_salad)
            item.append(data)
            data = {}
        if rib_eye != "":
            data["qty"] = int(rib_eye)
            data["unit_price"] = 72
            data['description_of_item'] = "300g Chilled Australian Rib Eye Steak"
            data['amount'] = 72 * int(rib_eye)
            item.append(data)
            data = {}
        if beef_ribs != "":
            data["qty"] = int(beef_ribs)
            data["unit_price"] = 65
            data['description_of_item'] = "Sticky BBQ Beef Ribs"
            data['amount'] = 65 * int(beef_ribs)
            item.append(data)
            data = {}
        if salmon_russian != "":
            data["qty"] = int(salmon_russian)
            data["unit_price"] = 23
            data['description_of_item'] = "Salmon Russian"
            data['amount'] = 23 * int(salmon_russian)
            item.append(data)
            data = {}
        claim_id=request.form.get("claim_id")
        if claim_id!="":
            dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
            claiming = dynamodb.Table('company_claim')
            response1 = claiming.get_item(
                Key={
                    'employee_claimID': claim_id
                })
            company = response1['Item']['companyID']
            get_company = dynamodb.Table('company')
            response2 = get_company.get_item(
                Key={
                    'companyID': company
                })
            the_companies=response2['Item']
            company_claim=the_companies['company_name']
            owner=response1['Item']['ownerID']
            new_id=dynamodb.Table('owner')
            the_list2=new_id.get_item(
                Key={
                    'ownerID':owner
                })
            the_list2=the_list2['Item']
            full_name=the_list2['first_name']+" "+the_list2['last_name']
            receipt2 = dynamodb.Table('company_claim')
            receipt_first = receipt2.scan()
            receipt_first = receipt_first['Items']
            data_value1=0
            for things in item:
                a=things['amount']
                data_value1+=a
            receipt={}
            receipt['receiptID']= "receipt_"+str(len(receipt_first))
            receipt['total_price']=data_value1
            receipt['companyID']="resource:org.acme.model.company#company13"
            receipt['total_cost'] = 0
            receipt['claim_tax_or_claim_company']='company_expenses'
            time1=time.asctime( time.localtime(time.time()))
            company_name='Jibby & Co'
            company_address= "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
            receipt_id=receipt['receiptID']
            logo="jibby.png"
            dumb_data_to_receipt_asset(receipt)
            claim_company_expenses(claim_id,receipt_id)
            receipt_pdf_generator(logo,receipt_id, company_name, company_address, full_name, time1, item, claim_id,company_claim)
            s3_setup(receipt_id + ".pdf")
            silentremove(receipt_id + ".pdf")
            update_claim(claim_id,data_value1)
            return rest_homepage()
        else:
            data_value1 = 0
            for things in item:
                a = things['amount']
                data_value1 += a
            receipt = {}
            receipt['receiptID'] = "receipt_" + "company13_" + str(len(the_receipt_id))
            receipt['total_price'] = data_value1
            receipt['companyID'] = "company13"
            receipt['total_cost']=0
            receipt['claim_tax_or_claim_company'] = 'company_expenses'
            time1 = time.asctime(time.localtime(time.time()))
            company_name = 'Jibby & Co'
            company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
            receipt_id = receipt['receiptID']
            logo = "jibby.png"
            dumb_data_to_receipt_asset(receipt)
            claim_id = ""
            full_name = ""
            company_claim = ""
            receipt_pdf_generator(logo,receipt_id, company_name, company_address, full_name, time1, item, claim_id,
                                  company_claim)
            s3_setup(receipt_id + ".pdf")
            silentremove(receipt_id + ".pdf")
            return rest_homepage()
        return rest_homepage()
    return rest_homepage()

@restaurant.route('/restaurant_homepage',methods=['GET','POST'])
def rest_homepage():
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    the_receipt = dynamodb.Table('receipt')
    the_receipt1 = the_receipt.scan()
    the_receipt1 = the_receipt1['Items']
    return render_template('restaurant.html', restaurant_data=the_receipt1, pdf_reader=pdf_reader_link)

def update_claim(claim_id,total_cost):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    claiming = dynamodb.Table('company_claim')
    response1 = claiming.get_item(
        Key={
            'employee_claimID': claim_id
        })
    get_claim = response1['Item']['claim_limit']
    claiming.update_item(
        Key={
            'employee_claimID': claim_id,
        },
        UpdateExpression = "set claim_limit = :r",
        ExpressionAttributeValues={
            ':r': (get_claim-total_cost)
        },
        ReturnValues="UPDATED_NEW"
    )


def claim_company_expenses(claim_id,receipt_id):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    transaction = dynamodb.Table('claim_company_expenses')
    transaction.put_item(
        Item={
            'transaction_id': claim_id,
            'receiptID': receipt_id,
            'claim_date_time':time.asctime( time.localtime(time.time()))
        })


def dumb_data_to_receipt_asset(data):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table1 = dynamodb.Table('receipt')
    table1.put_item(
        Item={
            'receiptID': data['receiptID'],
            'total_price': data['total_price'],
            'companyID': data['companyID'],
            'total_cost': data['total_cost'],
            'claim_tax_or_claim_company': data['claim_tax_or_claim_company']
        })


