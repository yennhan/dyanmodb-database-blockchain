# coding=utf-8
#Leow Yenn Han
#leowyennhan@gmail.com
import time,timeit,os,errno
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint
from SNP_pdf_generator import pdf_generator
from Loan_Agreement import pdf_loan_generator
import boto3
from botocore.client import Config

app = Flask(__name__)
Bootstrap(app)
s3_run= Blueprint('s3_run',__name__)

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def s3_setup(FILE_NAME):
    ACCESS_KEY_ID = 'AKIAJDHZRCD5D5BB33XQ'
    ACCESS_SECRET_KEY = '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'
    bucket_name = 'one-identity-pdf-storage'

    data = open(FILE_NAME, 'rb')
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    # Image Uploaded
    s3.Bucket(bucket_name).put_object(Key=FILE_NAME, Body=data, ContentType = " application/pdf",ACL='public-read')
    print ("Done")
