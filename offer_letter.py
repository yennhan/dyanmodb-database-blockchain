# coding=utf-8
#Leow Yenn Han
#leowyennhan@gmail.com
import time
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table,TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.lib.units import inch
from reportlab.lib.units import cm,mm
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from num2words import num2words
import io

PAGE_HEIGHT = defaultPageSize[1];PAGE_WIDTH = defaultPageSize[0]

def myFirstPage(canvas, doc):

    pageinfo = "platypus example"
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.setFont('Times-Roman', 9)
    canvas.restoreState()


def myLaterPages(canvas, doc):

    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d " % (doc.page))
    canvas.restoreState()

def pdf_offer_letter_generator(owner_id,loan_person,address,the_time,bank,amount,loan_duration,loan_duration_months,company_manager,saving_account,ic_no,hash_key):

    doc = SimpleDocTemplate(owner_id+".pdf",rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('Center', alignment=TA_LEFT, leftIndent=20))
    styles.add(ParagraphStyle('one', alignment=TA_LEFT, leftIndent=35))
    styles.add(ParagraphStyle('two', alignment=TA_JUSTIFY, leftIndent=20))
    styles.add(ParagraphStyle('t1', alignment=TA_JUSTIFY, leftIndent=20))
    styles.add(ParagraphStyle('left', alignment=TA_LEFT))
    Story = []
    logo = "UOB_logo.png"
    im = Image(logo, 3 * inch, 1 * inch, hAlign='LEFT')
    Story.append(im)
    Story.append(Spacer(1, 11))
    ptext = '<font size=11>DATE:  %s</font>' %(the_time)

    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11><b>%s</b><br/>%s<br/><br/>Dear Sir/Mdm,</font>' %(loan_person,address)

    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11><b><u>RE: APPLICATION FOR Home Flexi Smart FACILITY/LOAN</u></b></font>'
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11>We are pleased to inform you that your application for the HomeFlexi Smart("the Facility") has been approved by our Bank,%s ("the Bank"), subject to the following terms and conditions<br/><br/><u>HomeFlexi Smart</u></font>' %bank
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>Type of Loan</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>: Flexi Loan Facility</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3= '<font size=12>Loan Amount(TL)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>: %s</font>' %amount
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>Purpose</font>'
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = '<font size=12>: To finance the purchase of the Property(described hereafter)</font>'
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = '<font size=12>Description of the Property("the Property")</font>'
    ptext_7 = (Paragraph(ptext7, styles['left']))
    ptext8 = '<font size=12>: %s more particular described in the Deed of Assignment and/or the Sale and Purchase Agreement enetered into as between you and/or the vendor(s) or the developer(as the case maybe). In the event of any discrepancy or conflict between the description of the Property stated in the aforesaid Deed of Assignment and/or Sale and Purchase agreement, the description of the Property stated in the aforesaid Deed of Assignment and/or the Sale and Purchase Agreement shall prevail PROVIDED ALWAYS THAT the Property is acceptable to the Bank and the purchase price, area and the location of the Property stated in the Sale and Purchase Agreement shall be the same as that indicated by you to the Bank in your application for the Facility</font>' %address
    ptext_8 = (Paragraph(ptext8, styles['Justify']))

    able = [[ptext1, ptext_2],["",""],[ptext_3,ptext_4],["",""],[ptext_5,ptext_6],["",""],[ptext_7,ptext_8]]
    t = Table(able, (5.5 * cm, 10.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext="Availability Period"
    ptext1=(Paragraph(ptext,styles['Justify']))
    ptext2="The Faciltiy shall be made available for 36 or up to 60months (as the case may be) from the date of this Letter of Offer provided by always it shall not exceed the relevant period for the delivery of vacant posession of the Property as stated in the Sale and Purchase Agreement ('the Availbility Period')"
    ptext_2=(Paragraph(ptext2,styles['Justify']))
    ptext3 = "Tenure"
    ptext_3=(Paragraph(ptext3,styles['Justify']))
    ptext4 = "30 from the date of full disbursement of the loan; OR 60 from the date of this Letter of Offer as the case may be."
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "The Facility shall also be subject to periodic review at the discretion of the Bank and reapayble on demand"
    ptext_5=(Paragraph(ptext5,styles['Justify']))
    ptext6 = "Processing Fee:"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = ": Processing Fee is waived"
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    able = [[ptext1, ptext_2],["",""],[ptext_3,ptext_4],["",""],["",ptext_5],["",""],[ptext_6,ptext_7]]
    t = Table(able, (5.5 * cm, 10.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = 'Full terms and conditions applicable to the loan Facility are described in the attached Appendix'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = 'If the terms and conditions are acceptable to you, please indicate your acceptance by signing and returning the duplicate of this letter to us within fourteen(14) days from the date hereof, failing which this offer shall be considered as having lapsed and cancelled. Acceptance by you in signing and returning to the Bank the duplicate of this letter after the expiry date shall be treated by the Bank as a counter offer from you upon the exact term and conditions contained herein. Your said counter offer shall be deemed as accepted by the Bank, if the banking facility(ies) herein is/are subsequently made available to you by the Bank, provided always, that nothing herein shall be construed or intepreted as imposing upon the Bank the obligation to so accept your said counter offer.'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = 'Our Bank looks forward to a mutually beneficial relationship with you'
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11>Thank You.</font>'
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext = 'Yours Sincerely'
    Story.append(Paragraph(ptext, styles['left']))
    ptext = 'for %s' %bank
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<b>...........................</b>'
    Story.append(Paragraph(ptext, styles['left']))
    ptext = '<b>%s</b>' %company_manager
    Story.append(Paragraph(ptext, styles['left']))
    ptext = '<b>Credit Manager</b>'
    Story.append(Paragraph(ptext, styles['left']))
    ptext = '<b>Retail Credit Management</b>'
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = '<b>I/We accept the Offer based on the Terms and Conditions of the Letter of Offer and Appendix.</b>'
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))

    ptext = 'I/We hereby authorise the Bank to debit my/ our Loan / Overdraft / Current / Savings Account No %s (the "Designated Account") with the Bank for the payment of all disbursements/charges/fees/ monthly instalments/interest and any other expenses due to the Bank under the Facility. I/We undertake to ensure that sufficient funds are kept in the Designated Account to meet this payment. Where the Designated Account is a current account, I/We hereby understand and agree that it shall be my/our responsibility to ensure there is sufficient funds at all times in the Designated Account to honour cheques deposited for payment. I/We further acknowledge and agree that the Bank will not be held liable for defamation and or for breach of contract and or for any losses damages expenses costs or charges whatsoever which may be claimed against the Bank arising from remarks place on the return cheque(s) by the Bank and or upon the grounds that cheque(s) issued under the Designated Account was returned due to insufficient funds in the Designated Account as a result of the Bank debiting the Designated Acocunt pursuant to my/our above authorization.' %saving_account
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<b>I/We hereby authorize the Bank to the credit my Current / Savings Account No %s</b>' %saving_account
    Story.append(Paragraph(ptext, styles['left']))
    Story.append(Spacer(1, 11))
    ptext1='<b>Name</b>'
    ptext_1 = Paragraph(ptext1,styles['left'])
    ptext2 = '<b>IC No</b>'
    ptext_2 = Paragraph(ptext2, styles['left'])
    ptext3 = '<b>Digital Signature</b>'
    ptext_3 = Paragraph(ptext3, styles['left'])
    ptext4 = '<b>Date: </b>'
    ptext_4 = Paragraph(ptext4, styles['left'])
    ptext5= '%s' %loan_person
    ptext_5= (Paragraph(ptext5,styles['left']))
    ptext6= '%s' %ic_no
    ptext_6 = (Paragraph(ptext6, styles['left']))
    ptext7='%s' %hash_key
    ptext_7 = (Paragraph(ptext7,styles['left']))
    ptext8='%s' %the_time
    ptext_8 =(Paragraph(ptext8,styles['left']))
    able = [[ptext_1,ptext_2,ptext_3,ptext_4],[ptext_5,ptext_6,ptext_7,ptext_8]]
    t = Table(able, (4.5 * cm, 4.5 * cm, 3 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext="Please Contact our MSF Mortgage 04 Klang, Suite 06-01, Level 6 Centro, No 8 Jalan Batu Tiga Lima, 41300 Klang, Selangor Dahrul Ehsan, Malaysia on telephone 0333414653 or facsimile 03334107 for assitance "
    Story.append(Paragraph(ptext,styles['Justify']))
    doc.multiBuild(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

