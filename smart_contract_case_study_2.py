from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from Loan_Agreement import *
from offer_letter import *
from receipt_generator import *
from sys import stderr
import pprint,time




def calculate_cost(chick_breakie,jibby_big_breakfast,casa_egg,trio_drips,para_break,cala_salad,rib_eye,beef_ribs,salmon_russian):
    item = []
    data = {}
    stocks={}
    cost_of_dish=0
    if chick_breakie != '':
        data["qty"] = int(chick_breakie)
        data["unit_price"] = 30
        data['description_of_item'] = "Chick Breakie"
        data['amount'] = 30 * int(chick_breakie)
        amount=data['qty']
        id_1="stock_4_company13" #chicken sausage
        per_dish=2
        c=calculate_stock(id_1,amount,per_dish)
        meat_supplier(id_1)
        cost_of_dish+=c
        id_1 = "stock_2_company13"  # eggs
        per_dish = 2
        c=calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_16_company13"  # olive_oil
        per_dish = 1
        c =calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_17_company13"  # salt
        per_dish = 3
        c =calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 1
        c=calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        item.append(data)
        data = {}
    if jibby_big_breakfast != "":
        data["qty"] = int(jibby_big_breakfast)
        data["unit_price"] = 31
        data['description_of_item'] = "Jibby Big Breakfast"
        data['amount'] = 31 * int(jibby_big_breakfast)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_3_company13"  # chicken sausage
        per_dish = 2
        c=calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_13_company13"  # mushroom
        per_dish = 2
        c =calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_10_company13"  # bacon
        per_dish = 3
        cost_of_dish =calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        id_1 = "stock_19_company13"  # bread
        per_dish = 1
        c=calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_17_company13"  # salt
        per_dish = 3
        c=calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 1
        c=calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if casa_egg != "":
        data["qty"] = int(casa_egg)
        data["unit_price"] = 28
        data['description_of_item'] = "Casabalanca Egg"
        data['amount'] = 28 * int(casa_egg)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_2_company13"  # eggs
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_19_company13"  # bread
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if trio_drips != "":
        data["qty"] = int(trio_drips)
        data["unit_price"] = 22
        data['description_of_item'] = "Jibby Trio Drips"
        data['amount'] = 22 * int(trio_drips)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_2_company13"  # eggs
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_20_company13"  # sphaghetti
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_21_company13"  # tomato
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_8_company13"  # squid
        per_dish = 1
        c = calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if para_break != "":
        data["qty"] = int(para_break)
        data["unit_price"] = 25
        data['description_of_item'] = "Paradise Breakie"
        data['amount'] = 25 * int(para_break)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_19_company13"  # bread
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_2_company13"  # eggs
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_3_company13"  # chicken sausage
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_13_company13"  # mushroom
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if cala_salad != "":
        data["qty"] = int(cala_salad)
        data["unit_price"] = 22
        data['description_of_item'] = "Crispy Calamari Salad"
        data['amount'] = 22 * int(cala_salad)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_8_company13"  # squid
        per_dish = 1
        c = calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_11_company13"  # lettuce
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_10_company13"  # cabbage
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if rib_eye != "":
        data["qty"] = int(rib_eye)
        data["unit_price"] = 72
        data['description_of_item'] = "300g Chilled Australian Rib Eye Steak"
        data['amount'] = 72 * int(rib_eye)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_5_company13"  # rib eye
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_22_company13"  # onion
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_21_company13"  # tomato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    if beef_ribs != "":
        data["qty"] = int(beef_ribs)
        data["unit_price"] = 65
        data['description_of_item'] = "Sticky BBQ Beef Ribs"
        data['amount'] = 65 * int(beef_ribs)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_17_company13"  # salt
        per_dish = 5
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 8
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 4
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_6_company13"  # beef
        per_dish = 2
        c = calculate_stock(id_1, amount, per_dish)
        meat_supplier(id_1)
        cost_of_dish += c
        data = {}
    if salmon_russian != "":
        data["qty"] = int(salmon_russian)
        data["unit_price"] = 23
        data['description_of_item'] = "Salmon Russian"
        data['amount'] = 23 * int(salmon_russian)
        item.append(data)
        amount = data['qty']
        id_1 = "stock_17_company13"  # salt
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_18_company13"  # sugar
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        id_1 = "stock_23_company13"  # potato
        per_dish = 3
        c = calculate_stock(id_1, amount, per_dish)
        veggy_supplier(id_1)
        cost_of_dish += c
        data = {}
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    receipt = dynamodb.Table('receipt')
    receipt_first = receipt.scan()
    the_receipt_id = receipt_first['Items']
    data_value1 = 0
    for things in item:
        a = things['amount']
        data_value1 += a
    receipt = {}
    receipt['receiptID'] = "receipt_" + "company13_" + str(len(the_receipt_id))
    receipt['total_price'] = data_value1
    receipt['total_cost'] = int(cost_of_dish)
    receipt['companyID'] = "company13"
    receipt['claim_tax_or_claim_company'] = 'company_expenses'
    time1 = time.asctime(time.localtime(time.time()))
    company_name = 'Jibby & Co'
    company_address = "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
    receipt_id = receipt['receiptID']
    dumb_data_to_receipt_asset(receipt)
    claim_id=""
    full_name=""
    company_claim=""
    logo="jibby.png"
    receipt_pdf_generator(logo,receipt_id, company_name, company_address, full_name, time1, item, claim_id,
                          company_claim)
    s3_setup(receipt_id + ".pdf")
    silentremove(receipt_id + ".pdf")


def calculate_stock(id_1,amount,per_dish):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('stock')
    response1 = request_stock.get_item(
        Key={
            'stockID': id_1
        })
    the_list = response1['Item']
    current=the_list['stock_balance']
    request_stock.update_item(
        Key={
            'stockID': id_1
        },
        UpdateExpression="set stock_balance = :r",
        ExpressionAttributeValues={
            ':r': current-(amount*per_dish)
        },
        ReturnValues="UPDATED_NEW"
    )
    cost=float(the_list['price_per_unit'])*amount  #cost for this dish
    return cost

def meat_supplier(id_1):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('stock')
    response1 = request_stock.get_item(
        Key={
            'stockID': id_1
        })
    the_list = response1['Item']
    if the_list['stock_balance']<the_list['standard_level']:
       ask_restock_meat(id_1)


def veggy_supplier(id_1):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('stock')
    response1 = request_stock.get_item(
        Key={
            'stockID': id_1
        })
    the_list = response1['Item']
    if the_list['stock_balance'] < the_list['standard_level']:
        ask_restock_vege(id_1)

def ask_restock_vege(id_1):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('request_stock')
    get_restock = request_stock.scan()
    the_restock = get_restock['Items']
    request_stock.put_item(
        Item={
            'requeststockID': "requeststock_" + str(len(the_restock)),
            'stockID': id_1,
            'companyID': "company13",
            'supplierID': "supplier1",
            'restock_date_time_update': time.asctime(time.localtime(time.time())),
            'restock_status': "Required_restock"
        })


def ask_restock_meat(id_1):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    request_stock = dynamodb.Table('request_stock')
    get_restock = request_stock.scan()
    the_restock = get_restock['Items']
    request_stock.put_item(
        Item={
            'requeststockID':"requeststock_"+str(len(the_restock)),
            'stockID': id_1,
            'companyID': "company13",
            'supplierID': "supplier2",
            'restock_date_time_update': time.asctime(time.localtime(time.time())),
            'restock_status':"Required_restock"
        })


def dumb_data_to_receipt_asset(data):
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-1")
    receipt = dynamodb.Table('receipt')
    receipt.put_item(
        Item={
            'receiptID': data['receiptID'],
            'total_price': data['total_price'],
            'companyID': data['companyID'],
            'total_cost': data['total_cost']
        })


