
from flask import Flask, Blueprint, render_template

from flask_bootstrap import Bootstrap
from bank import banks
from s3_run import *
from sys import stderr
import pprint

app = Flask(__name__)
Bootstrap(app)
transaction = Blueprint('transaction',__name__)


pdf_reader_link ="https://s3-ap-southeast-1.amazonaws.com/one-identity-pdf-storage/"

'''
{u'$class': u'org.acme.model.TradeHouse',
  u'currentOwner': u'resource:org.acme.model.owner#owner1',
  u'h_transactedDateTime': u'2018-04-18T00:16:28.000Z',
  u'landtitle': u'resource:org.acme.model.LandTitle#land1',
  u'lawyer': u'resource:org.acme.model.Lawyer#lawfirm0',
  u'newOwner': u'resource:org.acme.model.owner#owner2',
  u'snp': u'resource:org.acme.model.s_n_p#snpowner1owner2',
  u'timestamp': u'2018-04-17T16:16:28.434Z',
  u'transactionId': u'94f77a88dadbf33735c8ae0a9b90dd4abc68de5f3ae71d626d84e12f1daccb84'}]
  '''

@transaction.route('/view_transaction',methods=['GET','POST'])
def view_transaction():
    get_loan_approval = requests.get(bank_loan_transaction+token)
    the_list = get_loan_approval.json()
    get_trade_house = requests.get(trade_house+token)
    the_list2 = get_trade_house.json()
    return render_template('Transactions.html',bank_list=the_list,tradehouse=the_list2)