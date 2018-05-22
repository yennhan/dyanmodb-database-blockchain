from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from Loan_Agreement import *
from offer_letter import *
from land_title_generator import *
from sys import stderr
import pprint,time


def snp_generate(selected_lawyer,agreed_price,land_title_id,owner1,new_owner):
    land_title = land_title_link + land_title_id + token
    the_owner = owner_post + owner1 + token
    the_new_owner=owner_post +new_owner+token
    get_owner = requests.get(the_owner)
    get_new_owner=requests.get(the_new_owner)
    get_land_title = requests.get(land_title)
    the_title = get_land_title.json()
    the_owner = get_owner.json()
    owner2 = get_new_owner.json()
    owner_id = the_owner['ownerID']
    datetime = time.asctime(time.localtime(time.time()))
    owner = the_owner['ownerID']+" "+the_owner['firstName'] + "" + the_owner['lastName']
    newOwner = owner2['ownerID']+" "+owner2['firstName']+""+owner2['lastName']
    NRIC = the_owner['nric']
    owner_address = 'NO 8, TR8/1,' + '<br/>' + ' 47400 Petaling Jaya'
    new_owner_address = 'NO 12, SS2/1,' + '<br/>' + ' 47300 Petaling Jaya'
    interest_rate = "Eight per centum (8%)"
    RPGT = "Three per centum (3%)"
    company=""
    property_description = "4 STOREY BUNGALOW"
    sold_house_address= the_title['no_lot']+" "+the_title['Daerah']+" "+the_title['Negeri']
    house_title=the_title['hakmilik_id'] +" "+the_title['no_lembaran_piawai']+" "+the_title['kategori_tanah']+" PHT. KL. 6/495/61"
    master_title = ""
    charge_or_assign = ""
    snp_id="snp"+the_owner['ownerID']+owner2['ownerID']
    data={}
    snp={}
    snp['snp_id']=snp_id
    snp['current_owner']=[]
    a="resource:org.acme.model.owner#%s" %the_owner['ownerID']
    snp['current_owner'].append(a)
    snp['new_owner']=[]
    b="resource:org.acme.model.owner#%s" %owner2['ownerID']
    snp['new_owner'].append(b)
    snp['landtitle']= "resource:org.acme.model.LandTitle#%s" %land_title_id
    snp['agreed_price']=float(agreed_price)
    snp['built_up_area']=float(the_title['luas_lot'])
    snp['transactionDateTime']=datetime
    print(snp)
    data['landtitle'] = "resource:org.acme.model.LandTitle#%s" %land_title_id
    data['snp'] = "resource:org.acme.model.s_n_p#%s" % snp_id
    data['currentOwner'] = "resource:org.acme.model.owner#%s" %the_owner['ownerID']
    data['newOwner'] = "resource:org.acme.model.owner#%s" %owner2['ownerID']
    data['lawyer'] = "resource:org.acme.model.Lawyer#%s" %selected_lawyer
    data["h_transactedDateTime"]= time.asctime(time.localtime(time.time()))
    post_to_tradehouse_blockchain(data)
    post_to_snp_asset(snp)
    pdf_generator(snp_id, datetime, owner, NRIC, newOwner, agreed_price, owner_address, new_owner_address,
                  interest_rate, RPGT, company, property_description, house_title, sold_house_address, master_title,
                  charge_or_assign)
    s3_setup(snp_id + ".pdf")
    silentremove(snp_id + ".pdf")
    return snp_id

def post_to_tradehouse_blockchain(data):
    headers = {'Content-type': 'application/json'}
    th = trade_house + token
    response = requests.post(th, json=data, headers=headers)

def post_to_snp_asset(data):
    headers = {'Content-type': 'application/json'}
    th = snp_url + token
    response = requests.post(th, json=data, headers=headers)
    print(response)


def land_title_generate(land_title_id,owner):
    land_title=land_title_link+land_title_id+token
    the_owner=owner_post+owner+token
    get_owner=requests.get(the_owner)
    the_1 = get_owner.json()
    get_land_title=requests.get(land_title)
    the_title=get_land_title.json()
    land_id = the_title['hakmilik_id']
    lot_no = the_title['no_lot']
    luas_lot=the_title['luas_lot']
    cukai_tahunan =the_title['cukai_tahunan']
    pelembaran_piawai = the_title['no_lembaran_piawai']
    land_usage= the_title['kategori_tanah']
    negeri = the_title['Negeri']
    daerah = the_title['Daerah']
    tempat = the_title['location_type']
    fail_number="PHT. KL. 6/495/61"
    owner_id = the_1['ownerID']
    NRIC = the_1['nric']
    name=the_1['firstName']+""+the_1['lastName']

    time1 = time.asctime(time.localtime(time.time()))
    land_title_pdf_generator(name,land_id, cukai_tahunan, negeri, daerah, bandar, tempat, lot_no, luas_lot, land_usage,
                             pelembaran_piawai, permohonan_ukur, fail_number, time1, tarik_pemberi, owner_id,
                             NRIC)
    s3_setup(land_id + ".pdf")
    silentremove(land_id + ".pdf")
    return land_id

def offer_letter_generator(loaner,bank,amount,loan_tenure,):
    check_loaner_ccris_ctos = owner_post + loaner + token
    bank_address = bank_url + bank + token
    get_bank = requests.get(bank_address)
    the_bank = get_bank.json()
    get_owner = requests.get(check_loaner_ccris_ctos)
    the_list = get_owner.json()
    data = {}
    first_name = the_list['firstName']
    last_name = the_list['lastName']
    NRIC = the_list['nric']
    full_name = first_name + "" + last_name
    borrower_address = 'NO 8, TR8/1,' + '<br/>' + ' 47400 Petaling Jaya'
    time1 = time.asctime(time.localtime(time.time()))
    loan_duration=loan_tenure*12
    p_i_c= the_bank["bankerID"]
    saving_account=" 112688111136"
    hash_key="12314smofs10649afomavo213ewofwlmofdv"
    owner_id = the_list['ownerID']
    offer="offer_"+owner_id
    pdf_offer_letter_generator(offer,full_name,borrower_address,time1,bank,amount,loan_tenure,loan_duration,p_i_c,saving_account,NRIC,hash_key)
    s3_setup(offer+".pdf")
    silentremove(offer+".pdf")
    return offer

def bank_loan_approval(loaner,bank,loan_tenure,loan_amount,flexi_loan):
    check_loaner_ccris_ctos=owner_post+loaner+token
    bank_address=bank_url+bank+token
    get_bank=requests.get(bank_address)
    the_bank=get_bank.json()

    get_owner = requests.get(check_loaner_ccris_ctos)
    the_list = get_owner.json()
    data={}
    owner_id = the_list['ownerID']
    ccris=the_list['ccris_score']
    ctos=the_list['ctos_score']
    NRIC=the_list['nric']
    bank1=the_bank['bankID']
    first_name=the_list['firstName']
    last_name=the_list['lastName']
    b_city=the_bank['bank_address']['city']
    b_street=the_bank['bank_address']['street']
    b_postalcode=the_bank['bank_address']['postalCode']
    b_postofficenumber=the_bank['bank_address']['postOfficeBoxNumber']
    full_bank_address= b_street+"<br/>"+b_postalcode+","+b_city+","+b_postofficenumber
    bank=the_bank['bank_name']

    full_name=first_name+""+last_name
    time1=time.asctime( time.localtime(time.time()) )
    if ccris <= 5 and ctos <= 5:
        data['owner']=owner_id
        data['the_approval'] = "Yes" #for asset loan agreement
        data['loan_id'] = 'loan_'+owner_id
        data['bank'] = bank1
        data['loan_term'] = loan_tenure
        data['loan_amount'] = loan_amount
        data['interest_rate'] = 4.5
        data['blr_rate'] = 4.0
        data['lock_in_period_in_year'] = 5
        data['penalty'] = 0
        data['rgbt'] = '.'
        data['flexi_loan'] = flexi_loan
        borrower_address = 'NO 8, TR8/1,' + '<br/>' + ' 47400 Petaling Jaya'
        document_name='loan_'+owner_id
        pdf_loan_generator(document_name,data['interest_rate'],data['loan_amount'],time1,str(full_name),NRIC,borrower_address,str(bank),full_bank_address)
        post_to_loan_blockchain(data)
        s3_setup(document_name+".pdf")
        silentremove(document_name+".pdf")
        return document_name
    elif ccris > 4:
        a="CCRIS score not approved"
        return a
    else:
        b="CTOS score not approved."
        return b

def post_to_loan_blockchain(data):
    headers = {'Content-type': 'application/json'}
    loan_post = loan_agreement + token
    response = requests.post(loan_post, json=data, headers=headers)
