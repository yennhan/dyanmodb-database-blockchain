from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from flask import send_from_directory
from owner import *
from land_title import *
from law_dashboard import *
from company_dashboard import *
from smart_contract_bank_loan import *
from loan_dashboard import *
from Transactions import *
from company_claim import *
from restaurant import *
from snp import *
from restaurant_2 import *
from stocks import *
from supplier1 import *
from supplier2 import *
from supplier3 import *
app= Flask(__name__)
Bootstrap(app)

app.register_blueprint(snp)
app.register_blueprint(banks)
app.register_blueprint(owner_port)
app.register_blueprint(land)
app.register_blueprint(law_dashboard)
app.register_blueprint(company)
app.register_blueprint(s3_run)
app.register_blueprint(loan)
app.register_blueprint(transaction)
app.register_blueprint(claim)
app.register_blueprint(restaurant)
app.register_blueprint(restaurant2)
app.register_blueprint(stocks)
app.register_blueprint(supplier1)
app.register_blueprint(supplier2)
app.register_blueprint(supplier3)
pdf_reader_link = "https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',loan="Apply Loan",display_offer_letter="display:none",display_loan= "display:none", display_snp="display:none",display_land_title="display:none")

@app.route('/trade_house',methods=['GET','POST'])
def tradehouse():
        #loan_amount = request.form.get('loanamount')
        #loan_tenure = request.form.get('loantenure')
        #flexi_loan = request.form.get('flexi_loan')
        #new_owner = request.form.get('newowner')
        #bank_required = request.form.get('banks')
        data={}
        document_name=bank_loan_approval(new_owner,bank_required,loan_tenure,loan_amount,flexi_loan)
        the_pdf=pdf_reader_link+document_name+".pdf"
        data['bankID']=bank_required
        data['loanID']=document_name
        data['ownerID']=new_owner
        data['b_transactedDateTime']=time.asctime( time.localtime(time.time()))
        dumb_data_to_transaction_bank(data)
        return render_template("dashboard.html",exist1='active',exist2="active",exist3="active",loan_ap = "Offer Letter Accepted",loan_agreement='%s'%the_pdf,display_snp="display:none")

@app.route('/generate_snp',methods=['GET','POST'])
def generate_snp():
    if request.method == 'POST':
        global document_name,agreed_price,the_pdf,the_land_pdf,new_owner,land_title_id, current_owner, new_owner, agreed_price, bank_required, loan_tenure, loan_amount, flexi_loan
        land_title_id = request.form.get('land_title_id')
        current_owner = request.form.get('owner1')
        new_owner = request.form.get('newowner')
        agreed_price = request.form.get('agreedprice')
        bank_required = request.form.get('banks')
        if bank_required == "":
            return render_template('dashboard.html', exist1='active', exist2='active', loan="No Loan Required")
        else:
            bank_required = request.form.get('banks')
            loan_amount = request.form.get('loanamount')
            loan_tenure = request.form.get('tenure')
            loan_tenure = int(loan_tenure)
            flexi_loan = request.form.get('flexi_loan')
            document_name = offer_letter_generator(new_owner, bank_required, loan_amount, loan_tenure)
            land_name_pdf=land_title_generate(land_title_id,current_owner)
            the_pdf = pdf_reader_link + document_name + ".pdf"
            the_land_pdf=pdf_reader_link+land_name_pdf+".pdf"
            return render_template("dashboard.html", exist1='active', status="blink_text",loan="Accept Offer Letter", exist2="active", loan_ap="Loan Approved!", offer_letter ='%s' % the_pdf ,display_loan="display:none",display_snp="display:none",land_name="%s"% the_land_pdf)


@app.route('/snp_complete',methods=['GET','POST'])
def snp_complete():
    if request.method=='POST':
        global panel_lawyer
        panel_lawyer = request.form.get('panel_lawyer')
        the_pdf = snp_generate(panel_lawyer,agreed_price,land_title_id,current_owner,new_owner)
        docs=pdf_reader_link+the_pdf+".pdf"
        the_pdf1 = pdf_reader_link + document_name + ".pdf"
        return render_template("dashboard.html", snp_agreement="%s"%docs, exist1='active', exist2="active", exist3="active", loan_ap="Loan Approved!", offer_letter ='%s' % the_pdf1 ,land_name="%s"% the_land_pdf)

@app.route('/journey_complete',methods=['GET','POST'])
def journey_end():
    the_pdf = snp_generate(panel_lawyer,agreed_price, land_title_id, current_owner, new_owner)
    docs = pdf_reader_link + the_pdf + ".pdf"
    the_pdf1 = pdf_reader_link + document_name + ".pdf"
    update_data_land(land_title_id,new_owner)
    return render_template("dashboard.html", snp_agreement="%s" % docs, exist1='active', exist2="active",
                           exist3="active",exist4="active",exist5="active", loan_ap="Loan Approved!", offer_letter='%s' % the_pdf1,
                           land_name="%s" % the_land_pdf)

def update_data_land(land_title_id, new_owner):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('land_title')
    table.update_item(
        Key={
            'hakmilik_id': land_title_id,
        },
        UpdateExpression="set ownerid = :r",
        ExpressionAttributeValues={
            ':r':new_owner
        },
        ReturnValues="UPDATED_NEW"
    )

def dumb_data_to_transaction_bank(data):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    table = dynamodb.Table('bank_loan_approval')
    table.put_item(
        Item={
            'transaction_id':data['bankID']+"_"+data['loanID'],
            'bankID': data['bankID'],
            'loanID': data['loanID'],
            'ownerID': data['ownerID'],
            'b_transactedDateTime': data['b_transactedDateTime']

        })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)