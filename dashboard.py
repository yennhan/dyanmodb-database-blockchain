# coding=utf-8
#Leow Yenn Han
#leowyennhan@gmail.com
import time,timeit,os,errno
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint
from SNP_pdf_generator import pdf_generator
from Loan_Agreement import pdf_loan_generator
import boto,boto3
from botocore.client import Config
from offer_letter import *

'''snp agreement post function possibility
#{
  "$class": "org.acme.model.s_n_p",
  "snp_id": "yo",
  "current_owner": "mike",
  "new_owner": "toto",
  "landtitle": "mike",
  "agreed_price": 0,
  "built_up_area": 0,
  "clauses": "string",
  "status": "EXPIRED"
}'''



owner_url = "http://ec2-13-229-79-37.ap-southeast-1.compute.amazonaws.com:3000/api/owner?access_token=6X2M38VE4bM8C2lXTqkXbv2JumycRqJOaF3U8eokrgrgK4bS1yvoGwIFm2qRwND2"
def import_data():
    #get_owner=requests.get(owner_url)
    #the_item=get_owner.json()
    #for x in range(len(the_item)):
        #pprint.pprint(the_item[x]['ownerID'])
    datetime             = time.ctime()
    owner                = ["Mike Leow","Dexter Leow"]
    NRIC                 = ['950228-10-1111','1234-1234-1234']
    newOwner             = "Hartanah AP Rakyat Berhad (Company No. 1232547-X)"
    agreed_price         = '1600000'
    build_up_size        = '5500sqft'
    owner_address        = 'NO 8, TR8/1,'+'<br/>'+' 47400 Petaling Jaya'
    new_owner_address    = "Suite 1606, Plaza Pengkalan, Jalan Tiong, 3rd Mile, Jalan Sultan Azlan Shah (Jalan Ipoh), 51100 Kuala Lumpur"
    interest_rate        = "Eight per centum (8%)"
    RPGT                 = "Three per centum (3%)"
    company              = "Hartanah AP Rakyat Sdn Bhd"
    property_description = "4 STOREY BUNGALOW"
    house_title          = "GERAN NO. HAKMILIK 127497 LOT 17265 MUKIM 12, DAERAH BARAT DAYA NEGERI PULAU PINANG"
    sold_house_address   = "33A, PERSIARAAN NURI 3, SETIA PEARL VILLA, 11900 BAYAN LEPAS, PULAU PINANG"
    master_title         = ""
    charge_assignee      = ""
    bank                 = "UNITED OVERSEAS BANK (MALAYSIA) BHD.(Company No. 271809 K)"
    bank_address = ""
    loan_ammount = '1600000'
    loan_margin = "4.5%"
    #pdf_generator(datetime,owner,NRIC,newOwner,agreed_price,build_up_size,owner_address,new_owner_address,interest_rate,RPGT,company,property_description,house_title,sold_house_address,master_title,charge_assignee)
    #pdf_loan_generator(loan_margin,loan_ammount,datetime,owner,NRIC,newOwner,agreed_price,build_up_size,owner_address,new_owner_address,interest_rate,RPGT,company,property_description,house_title,sold_house_address,master_title,charge_assignee,bank,bank_address)

def loan_offer_letter_data():
    loaner= "Mike Leow"
    address="NO 8, TR8/1,"+"<br/>"+" 47400 Petaling Jaya"+"<br/>"+"SELANGOR DAHRUL EHSAN "
    bank="UNITED OVERSEAS BANK (MALAYSIA) BHD.(Company No. 271809 K)"
    the_time=time.asctime( time.localtime(time.time()))
    amount="RM600,000"
    ic_no= "961223131-10-2313"
    loan_duration= 17
    loan_duration_months= loan_duration*12
    company_manager="AHMAD JAMALLUDIN BIN ABU BAKAR"
    saving_account = "112688111136"
    hash_key="231donsifw2jr3oefdmnsfoir0231koasmodq21"
    #pdf_offer_letter_generator(loaner,address,the_time,bank,amount,loan_duration,loan_duration_months,company_manager,saving_account,ic_no,hash_key)
#start=time.time()
#import_data()
#the_pdf = "SNP_12345.pdf"
#end = time.time()
#print (end-start)
loan_offer_letter_data()