from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import boto3
from receipt_generator import *
from smart_contract_case_study_2 import *
dynamodb = boto3.resource('dynamodb',region_name="ap-southeast-1")

a=[
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_0_company13",
    "companyID": "company13",
    "item_name": "Apple",
    "stock_balance": 300,
    "standard_level": 200,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_10_company13",
    "companyID": "company13",
    "item_name": "Bacon",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 4
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_11_company13",
    "companyID": "company13",
    "item_name": "Lettuce",
    "stock_balance": 300,
    "standard_level": 150,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_12_company13",
    "companyID": "company13",
    "item_name": "Flour",
    "stock_balance": 300,
    "standard_level": 150,
    "price_per_unit": 3.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_13_company13",
    "companyID": "company13",
    "item_name": "Mushroom",
    "stock_balance": 250,
    "standard_level": 50,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_14_company13",
    "companyID": "company13",
    "item_name": "Chicken thigh",
    "stock_balance": 200,
    "standard_level": 100,
    "price_per_unit": 8
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_15_company13",
    "companyID": "company13",
    "item_name": "Sweet_sauce",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 3
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_16_company13",
    "companyID": "company13",
    "item_name": "Olive Oil",
    "stock_balance": 550,
    "standard_level": 150,
    "price_per_unit": 2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_17_company13",
    "companyID": "company13",
    "item_name": "Salt",
    "stock_balance": 500,
    "standard_level": 150,
    "price_per_unit": 0.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_18_company13",
    "companyID": "company13",
    "item_name": "Sugar",
    "stock_balance": 600,
    "standard_level": 100,
    "price_per_unit": 0.6
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_19_company13",
    "companyID": "company13",
    "item_name": "Loaf_of_bread",
    "stock_balance": 400,
    "standard_level": 100,
    "price_per_unit": 2.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_1_company13",
    "companyID": "company13",
    "item_name": "Chicken Breast",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_20_company13",
    "companyID": "company13",
    "item_name": "Spaghetti",
    "stock_balance": 350,
    "standard_level": 100,
    "price_per_unit": 1.1
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_21_company13",
    "companyID": "company13",
    "item_name": "Tomato",
    "stock_balance": 350,
    "standard_level": 100,
    "price_per_unit": 0.7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_22_company13",
    "companyID": "company13",
    "item_name": "Onion",
    "stock_balance": 300,
    "standard_level": 100,
    "price_per_unit": 1.2
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_23_company13",
    "companyID": "company13",
    "item_name": "Potato",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 0.4
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_2_company13",
    "companyID": "company13",
    "item_name": "Egg",
    "stock_balance": 450,
    "standard_level": 100,
    "price_per_unit": 1
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_3_company13",
    "companyID": "company13",
    "item_name": "Beef Sausage",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 3
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_4_company13",
    "companyID": "company13",
    "item_name": "Chicken Sausage",
    "stock_balance": 250,
    "standard_level": 100,
    "price_per_unit": 2.5
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_5_company13",
    "companyID": "company13",
    "item_name": "Rib Eye Cut",
    "stock_balance": 300,
    "standard_level": 50,
    "price_per_unit": 6
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_6_company13",
    "companyID": "company13",
    "item_name": "Beef Ribs",
    "stock_balance": 300,
    "standard_level": 50,
    "price_per_unit": 7
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_7_company13",
    "companyID": "company13",
    "item_name": "Salmon_250g",
    "stock_balance": 150,
    "standard_level": 100,
    "price_per_unit": 11
  },
  {
    "$class": "org.acme.model.stock",
    "stockID": "stock_8_company13",
    "companyID": "company13",
    "item_name": "Squid",
    "stock_balance": 60,
    "standard_level": 20,
    "price_per_unit": 8
  }
]

table = dynamodb.Table('stock')
for i in range(len(a)):
  table.put_item(
    Item={
      'stockID':a[i]['stockID'],
      'companyID': a[i]['companyID'],
      'item_name': a[i]['item_name'],
      'stock_balance': a[i]['stock_balance'],
      'standard_level': a[i]['standard_level'],
      'price_per_unit': (str(a[i]['price_per_unit']))

})