import pymongo
import boto3
from botocore.client import Config
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb',region_name="ap-southeast-1")
import time


def add_owner_to_database():
    table = dynamodb.Table('user')
    table.put_item(
        Item={
            'ownerID': 'ruanb1',
            'first_name': 'ruan',
            'last_name': 'bekker',
            'age': 30,
            'account_type': 'administrator',
            'address':"none",
        }
    )
def write_to_owner():
    list = []
    the_list = []
    filename1 = "sample_of_50.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)
            the_list.append(list)
            list = []
    dump_data_owner(the_list)



def dump_data_owner(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('owner')
    for i in range(len(data)):
        table.put_item(
        Item = {
            'ownerID': data[i][2],
            'nric': data[i][1],
            'first_name': data[i][3],
            'last_name': data[i][4],
            'email_address':data[i][5],
            'type_of_employee': data[i][6],
            'income_amount': data[i][7],
            'ccris_score':data[i][8],
            'ctos_score':data[i][9]
        }
    )
def get_database():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('owner')
    response = table.scan()

def get_owner_database():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('owner')

    response = table.get_item(
        Key={
            'ownerID': 'ruanb1',
            'last_name': 'bekker'
        }
    )

    item = response['Item']
    name = item['first_name']

    print(item)
    print("Hello, {}".format(name))
def convert_to_json_land():
    data={}
    list = []
    the_list = []
    filename1 = "asset_of_50_land_title.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)
            the_list.append(list)
            list = []
    dumb_data(the_list)

def dumb_data(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('land_title')
    for i in range(len(data)):
        table.put_item(
            Item={
                'ownerid': data[i][0],
                'hakmilik_id': data[i][1],
                'cukai_tahunan': data[i][2],
                'Negeri': data[i][3],
                'Daerah': data[i][4],
                'location_type': data[i][5],
                'no_lot': data[i][6],
                'luas_lot': data[i][7],
                'kategori_tanah': data[i][8],
                'daftaran_pada':time.asctime( time.localtime(time.time()) ),
                'no_lembaran_piawai':data[i][9]
            }
        )
def add_lawyer_participant():
    data={}
    company=["Rahayu_Partnership","HS_LIM_&_CO","Donovan_&_Ho","JK_Lim_Advocates_&_Solicitors","Mirandah_Asia","MahWengKwai_&_Associates"]
    a=20
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('lawyer')
    for i in range(len(company)):
        table.put_item(
            Item={
                'lawfirmID':"lawfirm"+str(i),
                'lawyer_firm_id': "company"+str(a),
                'lawyer_id':  company[i]+"_lawyer_"+str(i),
                'company_lawyer_name': company[i],
            }
        )
        a+=1

def add_lawyer_company():
    data={}
    company=["Rahayu Partnership","HS LIM & CO","Donovan & Ho","JK Lim Advocates & Solicitors","Mirandah Asia","MahWengKwai & Associates"]
    a=20
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('company')
    for i in range(len(company)):
        b = "#owner" + str(a)
        table.put_item(
            Item={
                'companyID': "company_" + str(a),
                'company_name': company[i],
                'employee_in_this_company_ID': [b],
                'company_category': ["Law Firm"]
            }
        )
        a+=1

def write_company():
    data={}
    companies=["yilou","Prada","Shell","Petronas","PosLaju","Pizza_Hut","BestDengki","BMW","Mercedes","Toyota","Pemanis","Honda","CottonOn","Jibby&Co","Yahoo","Starbucks","IT_Solution","BCG","Exxon_Mobile","Accenture"]
    category=["F&B","Retail","Services","Services","Logistics","F&B","Eletronics","Automotives","Automotives","Automotives","F&B","Automotives","Retail&Fashion","F&B","MSC","F&B-Franchise","Consulting","Consulting","Oil&Gas","IT_solution"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('company')
    for i in range(20):
        a = "#owner" + str(i)
        table.put_item(
            Item={
                'companyID': "company"+str(i),
                'company_name': companies[i],
                'employee_in_this_company_ID': [a],
                'company_category': [category[i]]
            }
        )

def write_bank_id():
    bank_names=['Maybank','Bank Rakyat','UOB','RHB','HongLeong','Standard Chartered','HSBC','Affin','CIMB','Ambank','Citibank','Alliance Bank','Public Bank']
    file = open("asset_of_banks.txt", 'w')
    streets=["100 Jalan Tun Perak ","No.33, Jalan Rakyat","Jalan Raja Laut ","Jalan Tun Razak","6 Jalan Damanlela,Bukit Damansara","No. 30, Jalan Sultan Ismail","No 2 Leboh Ampang","80, Jalan Raja Chulan","Jalan Stesen Sentral 2","No. 8, Jalan Yap Kwan Seng","165 Jalan Ampang","No.8, Jalan Munshi Abdullah","146 Jalan Ampang"]
    postal_code=["50050","50470","50738","50400","50490","50250","50100","53300","50740","50450","50754","50100","50450"]
    p_o_box=["11057","11024","11212","10145","10510","unknown","10244","202","11751","10922","11725","163","12542"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bank')
    for i in range(len(bank_names)):
        table.put_item(
            Item={
                'bankID': "bank"+str(i),
                'bank_name':bank_names[i],
                'bankerID': "banker"+str(i),
                'bank_address': {"city":"Kuala Lumpur","country":"Malaysia","locality":"City","region":"SEA","street":streets[i],"postalCode":postal_code[i],"postOfficeBoxNumber":p_o_box[i]}
            }
        )





def dump_data_lawyer(data):
    return ""
#add_owner_to_database()
#get_owner_database()
#write_to_owner()
get_database()
#convert_to_json_land()
#create_table()
#write_company()
#add_lawyer_company()
#add_lawyer_participant()
#write_bank_id()
ACCESS_KEY_ID = 'AKIAJDHZRCD5D5BB33XQ'
ACCESS_SECRET_KEY = '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'
