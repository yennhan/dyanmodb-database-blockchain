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


def pdf_loan_generator(document_name,loan_margin,loan_ammount,datetime,borrower,NRIC,borrower_address,bank,bank_address):
    the_item = ''
    for item in range(len(NRIC)):
        the_item = the_item + NRIC[item]
    print(the_item)

    doc = SimpleDocTemplate("%s.pdf"%document_name, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)


    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add( ParagraphStyle('Center', alignment=TA_LEFT, leftIndent=20))
    styles.add(ParagraphStyle('one', alignment=TA_LEFT, leftIndent=35))
    styles.add(ParagraphStyle('two',alignment=TA_JUSTIFY,leftIndent=20))
    styles.add(ParagraphStyle('t1',alignment=TA_JUSTIFY,leftIndent=20))
    Story = []
    logo  = "UOB_logo.png"
    im    = Image(logo, 3* inch, 1.5 * inch, hAlign='CENTER')
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))


    ptext1  = '<font size=15><b>LOAN AGREEMENT<br/><br/>BETWEEN</b></font>'
    ptext_1 = Paragraph(ptext1, styles['Title'])
    ptext2  = '<font size=15><b>%s<br/><br/>AND<br/>%s<br/>%s</b></font>'% (bank,borrower,NRIC)
    ptext_2 = (Paragraph(ptext2, styles['Title']))

    able    = [['','',''],['','',''],['','',''],['',im,''],['','',''],['','',''],['',ptext_1,''],['','',''],['',ptext_2,''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','','']]
    t       = Table(able, (2.5 * cm, 12 * cm, 2.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=15><b>LOAN AGREEMENT</b></font>'
    Story.append(Paragraph(ptext, styles['Title']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>A LOAN AGREEMENT</b> dated the date as stated in Section 1 of the Schedule to this Agreement<br/><br/><br/><b>BETWEEN</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12><b>%s</b>  (referred to in this Agreement as “<b>the Bank</b>”), which has an address as stated in Section 2 of the Schedule to this Agreement, <br/><br/><br/><b>AND</b><br/><br/><br/><b>THE PARTY</b> (referred to in this Agreement as “<b>the Borrower</b>”) whose name, particulars and details are as stated in Section 3 of the Schedule to this Agreement.</font>' % bank
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))

    ptext   = '<font size=12><b>PART A</b><br/><br/><b>SECTION 1</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext   = '<font size=12>Section 1.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>The Housing Loan</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1,ptext_2]]
    t       = Table(able, (3* cm, 13* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext    = '<font size=12>1.1</font>'
    ptext1   = (Paragraph(ptext, styles['Justify']))
    ptext2   = '<font size=12>At the Borrower’s request, the Bank has agreed to lend the Borrower money to purchase a residential property upon the terms and conditions contained in the Letter of Offer and in this Agreement. It is a key term of this Agreement that the Borrower will offer the residential property as security to secure the repayment of the Housing Loan and payment by the Borrower of all amounts from time to time outstanding under the Letter of Offer and this Agreement.</font>'
    ptext_2  = (Paragraph(ptext2, styles['Justify']))
    able     = [[ptext1, ptext_2]]
    t        = Table(able, (1.5* cm, 14.5* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 1.2</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Purpose(s) of the Housing Loan</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>1.2</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>The Borrower must use the proceeds of the Housing Loan for the purposes of purchasing the Property and defraying any renovation costs incurred in relation to the Property and paying all insurance premiums on insurance policies which the Borrower may be required to take up and maintain in respect of the Property and paying any legal fees, costs and expenses incurred by the Borrower in relation to the Housing Loan.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 1.3</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Agreement to Borrow and Lend</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>1.3</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Subject to the terms and conditions of the Letter of Offer and this Agreement, the Bank has agreed to make available the Housing Loan to the Borrower on the basis of and in full reliance upon the warranties, representations and undertakings contained in Section 13.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    Story.append(PageBreak())
    ptext   = '<font size=12><b>SECTION 2</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 2.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Definitions</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>2.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>In this Agreement (both Part A and Part B inclusive), the following words have the meaning given to them below.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    event    = '<font size=10>“Event of Default" or<br/> “Events of Default”<br/><br/></font>'
    event_1  = (Paragraph(event, styles['Normal']))
    event2   = '<font size=10>“Housing Loan” or “Facility”<br/><br/></font>'
    event_2  = (Paragraph(event2, styles['Normal']))
    sub      = '<font size=11>i) immediately or in the future;<br/>  ii) upon the happening of any contingency;<br/>iii) as principal or as surety; or<br/>iv) solely or jointly with any other person; </font>'
    sub_1    = (Paragraph(sub,styles['Center']))
    ptext1   = '<font size=11><b>%s</b> and its successors in title and assigns.<br/><br/></font>' % bank
    ptext_1  = (Paragraph(ptext1,styles['Normal']))
    ptext2   = '<font size=11>i) The rate of interest stated by the Bank from time to time as its base lending rate, or<br/><br/> ii) If the term Base Lending Rate is no longer used, the rate of interest stated by the Bank to be applied for the purposes of this Agreement.<br/><br/></font>'
    ptext_2  = (Paragraph(ptext2, styles['Normal']))
    ptext3   = '<font size=11>The person named in this Agreement as borrower of the Housing Loan whose name, particulars and details are as stated in Section 3 of the Schedule to this Agreement.<br/><br/></font>'
    ptext_3  = (Paragraph(ptext3, styles['Normal']))
    ptext4   = '<font size=11>A day when banks are open for general banking business in the state where the Bank is located.<br/><br/></font>'
    ptext_4  = (Paragraph(ptext4, styles['Normal']))
    ptext5   = '<font size=11>The default rate of interest applicable to the Housing Loan as stated in the Letter of Offer.<br/><br/></font>'
    ptext_5  = (Paragraph(ptext5, styles['Normal']))
    ptext6   = '<font size=11>Any of the events, situations or circumstances set out in Section 8.1 of this Agreement.<br/><br/></font>'
    ptext_6  = (Paragraph(ptext6, styles['Normal']))
    ptext7   = '<font size=11>a) The principal amount in the sum set out in Section 4 of the Schedule that the Bank has agreed to lend to the Borrower under this Agreement; and<br/><br/>b) Where applicable, this shall include other facilities previously lent or hereafter agreed to be lent by the Bank pursuant to Sections 7.2 and 7.3<br/><br/></font>'
    ptext_7  = (Paragraph(ptext7, styles['Normal']))
    ptext8   = '<font size=11>All money outstanding or payable by the Borrower under the Security Documents in connection with the Housing Loan:- <br/><br/> (a) whether such money is payable:-<br/><br/> </font>'
    ptext_8  = (Paragraph(ptext8, styles['Normal']))
    ptext9   = '<font size=11><br/>(b) including principal, interest, additional interest, charges, commission and other costs; and<br/><br/> </font>'
    ptext_9  = (Paragraph(ptext9, styles['Normal']))
    ptext10  = '<font size=11>(c) including where applicable, monies referred to in Sections 7.2 and 7.3<br/></font>'
    ptext_10 = (Paragraph(ptext10, styles['Normal']))
    able     = [['"Bank"',ptext_1],['"Base Lending Rate"',ptext_2],['"Borrower"',ptext_3],['"Banking Day"',ptext_4],['"Default Rate"',ptext_5] ,[event_1,ptext_6],[event_2,ptext_7],['"Indebtedness"',(ptext_8,sub_1,ptext_9,ptext_10)]]
    t        = Table(able, (4 * cm, 11.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext   = "<font size=11> a) The Letter of Offer including any amendments or supplements thereto issued by the Bank and accepted by the Borrower containing the main terms and conditions upon which the Bank has agreed to provide the Housing Loan to the Borrower;<br/><br/>b) In the event of conflict or discrepancy between the terms and conditions of the Letter of Offer and this Agreement, the terms and conditions of the Letter of Offer shall prevail; and<br/><br/>c) Where applicable, the term “Letter of Offer” shall refer to:-<br/><br/></font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2  = "<font size=11>The period stated in the Letter of Offer during which the Bank may impose an early termination fee on the Borrower for repaying any part of, or the entire, Indebtedness pursuant to Section 6.1(c).<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Normal']))
    ptext3  = "<font size=11>As set out in Section 5 of the Schedule.<br/><br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4  = "<font size=11>The rate of interest, being the sum of the Base Lending Rate and the Margin, that is applicable to the Housing Loan or such other rate of interest that the Bank may prescribe at any time.<br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Normal']))
    ptext5  = "<font size=11>The piece of land or the lease of the land or the parcel/unit of immovable property identified or described in Section 6 of the Schedule together with all buildings and fixtures and on such land or property.<br/><br/></font>"
    ptext_5 = (Paragraph(ptext5, styles['Normal']))
    ptext6  = "<font size=11>The lawful currency of Malaysia.<br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Normal']))
    ptext7  = "<font size=11>The Letter of Offer, this Agreement and such other security documents that have been or will be executed by the Borrower to secure the repayment of the Housing Loan by the Borrower as well as the payment of other Indebtedness.<br/><br/></font>"
    ptext_7 = (Paragraph(ptext7, styles['Normal']))
    sub     = "<font size=11>(i) the first letter of offer accepted by the Borrower and set out in Part C hereto; and/or<br/><br/>(ii) any one of the letter(s) of offer for additional or further facility(ies); and/or<br/><br/>(iii) any letter(s) for the variation, restructuring, conversion, interchange or substitution of the first Housing Loan or Facility or additional or further facility(ies).<br/><br/></font>"
    sub_1   = (Paragraph(sub, styles['Center']))
    able    = [['"Letter of Offer"', (ptext_1,sub_1)], ['"Lock-in Period"', ptext_2], ['"Margin"', ptext_3], ['"Prescribed Rate "', ptext_4],['"Property "', ptext_5],['“Ringgit Malaysia”; “RM”', ptext_6],['"Security Documents"', ptext_7]]
    t       = Table(able, (4.2 * cm, 11.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=13><b>PART A</b><br/><br/><b>SECTION 3</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 3.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Conditions Precedent to Drawing</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>3.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>The Bank may not release any part of the Housing Loan unless it has satisfactory evidence of the following being fulfilled:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext   = "<font size=11><br/> a) </font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2  = "<font size=11><br/>the conditions set out in the Letter of Offer and/or this Agreement, and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Normal']))
    able    = [[ptext_1, ptext_2]]
    t       = Table(able, (0.8* cm, 12.4* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext3  = "<font size=11> b) </font>"
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4  = "<font size=11>the additional conditions precedent set out in the Letter of Offer.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Normal']))
    able    = [[ptext_3, ptext_4]]
    t       = Table(able, (0.8 * cm, 12.4 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 3.2</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Cancellation of the Housing Loan</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>3.2</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>If the Borrower does not comply with any condition within the time stated by the Bank, the Bank is entitled to cancel the Housing Loan.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 3.3</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Waiver of Conditions</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>3.3</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>The conditions set out in this Section are inserted for the sole benefit of the Bank. The Bank may waive compliance with any of the conditions in this Section without affecting its rights under this Agreement. Such waiver does not prevent the Bank from later demanding the Borrower to comply with any or all of the waived conditions within any period notified by the Bank to the Borrower.<br/><br/>No waiver of any conditions precedent constitutes a waiver of any other conditions precedent except to the extent expressly provided in such waiver.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=13><br/><br/><b>SECTION 4</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext   = '<font size=12>Section 4.1</font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12>Payment of Interest</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>(a)</font>'
    ptext1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = '<font size=12>The Borrower must pay (without the requirement of notice from the Bank) interest at the relevant Prescribed Rate and where applicable, the Default Rate, to the Bank on such amount of the Housing Loan specified in the Letter of Offer up to the date when the Housing Loan is fully repaid to the Bank.<br/><br/></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4 = '<font size=12>Unless otherwise notified by the Bank to the Borrower, interest is to be debited to the Borrower’s account on the last day of every month.<br/><br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>(c)</font>'
    ptext_5 = (Paragraph(ptext5, styles['Normal']))
    ptext6 = '<font size=12>Interest is payable monthly in arrears, or at such other period as the Bank may prescribe.<br/><br/></font>'
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=12>Section 4.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Calculation of Interest</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>(a)</font>'
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = '<font size=12>Interest is calculated on the basis of the actual number of days elapsed and based on a 365-day year.<br/><br/></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4 = '<font size=12>Interest for this Housing Loan will be calculated on a daily/monthly/periodic rest basis as indicated in the Letter of Offer, unless otherwise stated or agreed by the Bank, and is payable in the manner stated by the Bank.<br/><br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>(c)</font>'
    ptext_5 = (Paragraph(ptext5, styles['Normal']))
    ptext6 = '<font size=12>Interest will be calculated in accordance with the Bank’s usual practice, having regard amongst others, the nature of the Housing Loan, up to the date of full payment.<br/><br/></font>'
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = '<font size=12>(d)</font>'
    ptext_7 = (Paragraph(ptext7, styles['Normal']))
    ptext8 = '<font size=12>Interest will be charged on all outstanding under the Housing Loan.<br/><br/></font>'
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able = [[ptext_1, ptext_2], [ptext_3, ptext_4], [ptext_5, ptext_6],[ptext_7,ptext_8]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 4.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Default Rate</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>4.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>If the Borrower fails to pay any amount payable under the Housing Loan on the due date (including amounts payable following a termination of the Housing Loan), the Borrower must pay the Bank interest at the Default Rate on the entire overdue amount. Interest at the Default Rate is calculated from the due date until the date of actual payment (both before and after court judgment).</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 4.4</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Variation of Interest Rate</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext1 = '<font size=12>(a)</font>'
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2 = '<font size=12>Regardless of any other provisions in this Agreement, the Bank is entitled to vary at any time:-<br/><br/>(i) the interest rate and the manner of calculation of the interest rate; and<br/>(ii) any commission, discount or other banking charges.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>Such variation may be made in respect of the following:-<br/><br/>(i) Base Lending Rate; or<br/>(ii) the Margin; or <br/>(iii) any other reference rate used in any Letter of Offer; or <br/>(iv) any other rate of interest specified by the Bank;<br/><br/>or a combination of any one or more of the methods of calculation of interest, including changing the basis on which the Prescribed Rate or the Default Rate is arrived at.</font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>(c)</font>'
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = '<font size=12>The amended or new Prescribed Rate or commission, discount or banking charges is payable from the date such amended or new Prescribed Rate, commission, discount or other banking charges take(s) effect. Interest will be re-calculated, if necessary in accordance with the provisions of this Agreement.</font>'
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = '<font size=12>(d)</font>'
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    ptext8 = '<font size=12>The Bank will give at least 21 calendar days’ prior notice of change of the Prescribed Rate, or the new commission, discount or banking charges to the Borrower but the Borrower’s non-receipt of the notice will not affect or invalidate any change. Notice by the Bank may be given:-<br/><br/>(i) in accordance with the “Notice” provisions set out in Section 11 of this Agreement; or<br/>(ii) by general advertisement in any form(s) of mass communication; or<br/>(iii) by notice in the Bank’s website and/or placed at the banking hall of the<br/>Bank’s branches.<br/><br/></font>'
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9 = '<font size=12>(e)</font>'
    ptext_9 = (Paragraph(ptext9, styles['Justify']))
    ptext10 = '<font size=12>If the Prescribed Rate payable on the Housing Loan is varied and the Housing Loan is repayable in instalments, the Bank may:-<br/><br/>(i) vary the amount of such Instalments; or<br/>(ii) vary the number of Instalments; or<br/>(iii) vary both.<br/><br/></font>'
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3, ptext_4],[ptext_5, ptext_6],[ptext_7, ptext_8],[ptext_9, ptext_10]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 4.5</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Capitalisation of Interest</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>4.5</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Interest on any amounts secured under the Security Documents (including capitalised interest), is to be capitalised and added to the principal sum then owing at the end of each calendar month or as determined by the Bank. The total sum will then bear interest at the relevant Prescribed Rate and/or where applicable Default Rate. This total sum shall be secured and payable accordingly, whether before or after court judgment or demand for payment has been made on the Borrower.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 4.6</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Capitalised Interest excluded from Limit or Principal</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>4.6</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>For the purpose of ascertaining whether the limit of the principal amount has been exceeded or not, all accumulated and capitalised interest are deemed to be interest and not principal sum.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 4.7</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Loan Statement</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>4.7</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The Bank will provide a loan statement to the Borrower at least once a year indicating the outstanding balance at the beginning and end of the period covered by the statement, the amount credited and charged, including interest and other non-interest charges, and the dates when those amounts were posted to the account.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=13><br/><br/><b>SECTION 5</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 5.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Repayment</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext1 = '<font size=12>(a)</font>'
    ptext_1 = (Paragraph(ptext1, styles['Normal']))
    ptext2 = '<font size=12>Regardless of any provision of this Agreement, the Housing Loan is immediately repayable upon demand by the Bank in writing upon the occurrence of an Event of Default.<br/><br/></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4 = '<font size=12>Until such a demand is made by the Bank, the Housing Loan is repayable at the dates and in such manner as stated in the Letter of Offer.<br/><br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_1, ptext_2], [ptext_3, ptext_4]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    Story.append(PageBreak())
    ptext = '<font size=12>Section 5.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Re-drawing or Re-borrowing</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext1 = '<font size=12>5.2</font>'
    ptext_1 = (Paragraph(ptext1, styles['Normal']))
    ptext2 = '<font size=12>The Bank may at its absolute discretion subject to the terms and conditions set out in Part B or as the case may be, Letter of Offer allow the Borrower to redraw or re-borrow any of the amounts repaid or prepaid. Such amounts redrawn or re- borrowed together with interest thereon at the applicable Prescribed Rate shall be deemed to be and form part of all the monies owing or payable by the Borrower and secured by the Security Documents.<br/><br/></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1.5 * cm, 14.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=13><br/><b>SECTION 6</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 6.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Prepayment and Early Settlement</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>(a)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>If:-<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = "<font size=11>the Borrower wishes to repay any part of the Indebtedness or the Housing Loan before its due date; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Normal']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext3 = "<font size=11> (ii) </font>"
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4 = "<font size=11>such early repayment is permitted under the Letter of Offer,</font>"
    ptext_4 = (Paragraph(ptext4, styles['Normal']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext4 = '<font size=12>the Borrower must provide such period of notice as may be stated in the Letter of Offer to the Bank.<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>The Borrower may repay any part of the Indebtedness or the Housing Loan in multiples of the prepayment sum as the Bank may in its absolute discretion accept.<br/><br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>(c)</font>'
    ptext_5= (Paragraph(ptext5, styles['Justify']))
    ptext6 = '<font size=12>If the Borrower repays any part of, or the entire, Indebtedness or the Housing Loan during the Lock-in Period, the Bank shall charge the Borrower an early termination fee which reflects a reasonable estimate of the costs incurred by the Bank as a result of such early termination. Such costs may include:-<br/></font>'
    ptext_6= (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_3, ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = "<font size=11>costs that have not been recovered because of a financing contract with discounted rate during the Lock-in Period is terminated early; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = "<font size=11>initial costs that have not been recovered.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Normal']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 6.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Application of Prepayment Sum</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>6.2</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>All prepayments received by the Bank are to be applied by the Bank in or towards repayment of the Housing Loan in the inverse order of maturity.<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = '<font size=12>Section 6.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Partial Repayment</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>6.3</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>Partial repayments of the Housing Loan do not relieve the Borrower of any of the Borrower’s obligations under this Agreement, except to the extent of the total amounts prepaid.<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=13><br/><b>SECTION 7</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 7.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Stamp Duties, Registration Fees and Other Costs</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>(a)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>The Borrower must on demand pay the Bank:- <br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10>all costs and expenses (including legal fees, stamp duties, disbursements and any related penalties) the Bank incurs in connection with the preparation, execution, registration or perfection of the Security Documents;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10>all costs and expenses (including legal fees on a solicitor-client basis, stamp duties, disbursements and any related penalties) the Bank incurs in connection with:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (1) </font>"
    ptext_1 = (Paragraph(ptext, styles['two']))
    ptext2 = "<font size=10>the enforcement or the preservation of any rights under the Security Documents; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1.7 * cm, 10 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (2) </font>"
    ptext_1 = (Paragraph(ptext, styles['two']))
    ptext2 = "<font size=10>the Bank’s involvement with any legal proceedings to protect, or connected to, the Property or any account(s) of the Borrower.</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (1.7 * cm, 10 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext4 = '<font size=12>All such amounts are payable by the Borrower on a full indemnity basis. Such payment must be made together with interest from the date the costs and expenses are incurred to the date of full payment at the Prescribed Rate and if applicable, the Default Rate (both before and after judgment).<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>(b)</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>Legal costs and expenses on a full indemnity basis are payable by the Borrower regardless of whether the Housing Loan is cancelled or aborted at any time before completion of legal documentation. <br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 7.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Upstamping</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>7.2</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>In the event that the total monies advanced to or due and owing by the Borrower to the Bank shall at any time exceed the principal limit for which ad valorem stamp duty had been paid, this Agreement or the Letter of Offer shall be upstamped with ad valorem duty to cover the excess. The stamp duty including any penalty incurred shall form part of the monies owing or payable by the Borrower and secured by the Security Documents.<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    Story.append(PageBreak())
    ptext = '<font size=12>Section 7.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Principal and Secondary Instrument</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>7.3</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>The Letter of Offer, this Agreement and the Security Documents are instruments employed in one transaction to secure the Indebtedness. Ad valorem stamp duty had been paid from time to time on the original of this Agreement and/or any supplements thereto, and/or the Letter of Offer and/or the Security Documents within the meaning of Section 4(3) of the Stamp Act, 1949. For the purpose of the said Section 4(3) of the Stamp Act, this Agreement shall be deemed the primary or principal instrument and the Letter of Offer and/or Security Documents are deemed the auxiliary or secondary instruments.<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=13><b>PART A</b><br/><br/><b>SECTION 8</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Section 8.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Events of Default</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext3 = '<font size=12>8.1</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12>The Borrower is deemed to have committed a default under the Security Documents, if the Borrower commits or threatens to commit a breach of any of the covenants, undertakings, stipulations, terms, conditions, or provisions stated under the Security Documents, or upon the happening of any one or more of the following events:-<br/></font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (a) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10><u>Non-payment</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2],['','The Borrower fails or defaults in the payment of any sum of money']]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
     #   ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=11>on its due date, whether formally demanded or not; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
     #   ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
     #   ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>(if due on demand) when demanded by virtue of the provisions of the Security Documents; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,12))
    ptext = "<font size=11> (b) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10><u>Breach of Other Terms and Conditions</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2], ['', 'The Borrower:-']]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>breaches any term of the Security Documents or in any document delivered under the Housing Loan or the Security Documents; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>fails to comply with any notice given under any of the Security Documents requiring him to remedy any breach of the terms of such Security Document; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
     #   ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (c) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10><u>Breach of Representation and Warranties</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2], ['', 'Any representation or warranty made or implied under:-']]
    t = Table(able, (1 * cm, 11 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Section 13 or any other provision of this Agreement; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    Story.append(PageBreak())
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>any notice, certificate, letter or other document delivered under this Agreement,</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext2 = "<font size=10>is incorrect or misleading (as determined by the Bank) in a material detail as of the date on which it was made or deemed to have been made; or<br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_2]]
    t = Table(able, (2.5* cm, 12.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
      #  ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
      #  ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (d) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Ability of the Borrower to Perform Terms in Security Documents</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>Any event(s) has/have occurred, or a situation exists (including changes in the financial condition of the Borrower), which might, in the opinion of the Bank, affect the ability of the Borrower to perform his obligations under the Security Documents; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (e) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Validity of the Security Documents</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>The validity of any of the Security Documents is challenged by any person; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (f) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Security in Jeopardy</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>The Bank is of the opinion that any of the security created pursuant to the Security Documents is in jeopardy or the value of the security created pursuant to the Security Documents is insufficient for the Bank’s purpose upon valuation or re-valuation; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (g) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Illegality</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>It is or will become unlawful for the Borrower to perform or comply with any one or more of the obligations of the Borrower under the Security Documents; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (h) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Authorisation and Consents</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>Any action, condition, consent or thing at any time required to be taken, fulfilled or done for any of the purposes stated in Section 13.1.5:-<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>is not taken, fulfilled or done; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>ceases to be in full force and effect without modification; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Breach of Other Loans</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>The Borrower; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Any company deemed by the Bank to be associated to the Borrower by way of effective equity interest and/or managementcontrol; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Any company in which the Borrower is deemed by the Bank to hold a controlling interest (whether by way of shareholding, or whether it is by reason that such company is accustomed or is under an obligation to act in accordance with the Borrower’s directions, interest or wishes),</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext2 = "<font size=10>commits a default of any provision of any agreement, or security documents, or both (as the case may be) relating to other accounts or loan facilities granted by other parties; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['','', ptext_2]]
    t = Table(able,(0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = "<font size=11> (j) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Cross Default</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Any other indebtedness of the Borrower becomes payable or due prematurely, or becomes capable of being declared payable or due prematurely, by reason of a default by the Borrower in its obligations with respect to that indebtedness; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>The Borrower fails to make any payment in respect of that indebtedness on the due date for such payment, or if due on demand when demanded; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Upon the security for any such indebtedness becoming enforceable; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (k) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Legal Proceedings</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>Any legal proceedings, suit or action of any kind whatsoever (whether criminal or civil) is instituted against the Borrower; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (l) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Enforcement Proceedings</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>A distress or execution or other process of a court of competent jurisdiction is levied upon or issued against all or any part of the property of the Borrower and such distress, execution or other process is not discharge by the Borrower within five (5) days from the date of such levy or issue; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (m) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Insolvency</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', 'The Borrower ']]
    t = Table(able, (1* cm,1.9*cm, 12.9 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>becomes insolvent or is adjudged a bankrupt; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>is unable to pay its debts as they fall due; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>stops or suspends, or threatens to stop or suspend, payment of all or a material part of its debts; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (iv) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>begins negotiations or takes any proceeding or other step with a view to readjustment, rescheduling or deferral of all or any part of its indebtedness; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (n) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Bankruptcy</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', 'The Borrower:-']]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>Any step or action is taken for the bankruptcy of the Borrower; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>A petition for bankruptcy is presented against the Borrower; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>If such proceeding or action has been taken by or against the Borrower, that step or petition is not discharged or stayed within twenty-one (21) days from the date of the taking of the step or petition; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (o) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Assignment</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', 'The Borrower ']]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>makes an assignment for the benefit of its creditors; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,(2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>enters into an arrangement for composition for the benefit of its creditors; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,(2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>allows any judgment against him to remain unsatisfied for a period of fourteen (14) days or more, unless an appeal against the judgment is pending and a stay of execution has been granted; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (p) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Moratorium on payments</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', 'The Borrower ']]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>enters into or proposes to enter into; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able, (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>there is declared by any competent court or authority,</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext2 = "<font size=10>a moratorium on the payment of Indebtedness or other suspensions of payments generally; or<br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['','',ptext_2]]
    t = Table(able,(0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
       # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (q) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Compulsory acquisition</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>A notice or proposal for compulsory acquisition of all or any of the assets of the Borrower is issued or made under or by virtue of an Act of Parliament or other statutory provision; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (r) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Death and Insanity</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>The Borrower dies or becomes insane; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (s) </font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=10><u>Material Adverse Change</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>Any event or series of events (whether within or outside of Malaysia and whether of a national or international nature) including any act of violence, terrorism, hostility or war or endemic or epidemic or other calamity occurs which in the Bank’s opinion:-<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>could or might affect the Borrower’s ability or willingness to fully comply with all or any of his obligations under any of the Security Documents or make it improbable that the Borrower would be able to do so; or or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>would render it inadvisable or impractical for the Bank to make or continue to make the Facility available or allow any use of the Facility; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>could or might jeopardize the Facility or any of its security or the Bank’s security position; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (t) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Use of Housing Loan not for purposes stated</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>The Housing Loan is not used for the purposes stated or the Housing Loan is used for illegal or speculative purposes; or<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = "<font size=11> (u) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Borrower’s Account re-designated or closed</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>If the Borrower's account is re-designated or closed by the Bank as a result of:-<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able,(0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>any guideline or directive; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>the account having been conducted unsatisfactorily; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>he account having been suspended due to a court order or at law; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = "<font size=11> (iv) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>an investigation by the Bank giving rise to negative findings including dishonesty, fraud or suspicious activities; or</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['',ptext_1, ptext_2]]
    t = Table(able,  (2* cm, 2.3 * cm, 11.2 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(PageBreak())
    ptext = "<font size=11> (v) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Security Document not perfected</u><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=10>If any of the Security Documents cannot be perfected for any reason whatsoever or if any Security Document which requires to be registered, cannot be registered or is invalid for any reason whatsoever.<br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    able = [['',ptext_1, ptext_2], ['','', ptext_3]]
    t = Table(able, (0.8* cm,1.7*cm, 12.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=12><b>SECTION 9</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>Section 9.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Rights of Bank on Default</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>(a)</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>If any of the events described in Section 8.1 occurs,</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>the Bank is entitled to immediately suspend further utilisation of any or all of the Housing Loan, or to reduce the limit or amount made available under the Housing Loan, without having to make a prior demand; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>the Indebtedness will become and be deemed to be immediately due and payable, regardless of any provision of this Agreement to the contrary.</font>"
    ptext_2 = (Paragraph(ptext2, styles['two']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>(b)</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>If any of the events set out in Section 8.1 occurs, the Bank is also entitled to take such action (whether on its own accord or through its agent(s)) as may be appropriate against the Borrower, including:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>action to recall the Housing Loan or to sue for the recovery of the Indebtedness either before, after or concurrently with the action to enforce any of the Security Documents; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>to apply any credit balance in whatever currency standing to any account of the Borrower with any office or branch of the Bank or any member of the Bank’s group of companies, towards satisfaction of the Indebtedness.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>(c)</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Any part of the Housing Loan not disbursed or utilised before the default may be cancelled by the Bank. Upon such cancellation, any part of the Housing Loan already disbursed or utilised will become due and immediately repayable on demand, regardless of any provision of this Agreement to the contrary.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12>Section 9.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Proceeds of Recovery</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>9.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Subject to statutory priorities (if any), all amounts received by the Bank from any proceeding instituted or step taken under any of the Security Documents are to be applied by the Bank:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext   = "<font size=10> FIRSTLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2  = "<font size=10>in payment of any rents, taxes, assessments, fees, lawful outgoings and other fees due and payable to the relevant authorities by the Borrower in respect of the Property charged or assigned to the Bank as security for the Housing Loan;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [['',ptext_1, ptext_2]]
    t       = Table(able, (2.3 * cm, 3.6 * cm, 10.3* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> SECONDLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in the enforcement of any of the Security Documents or in the performance of any duties or the exercise of any powers vested in the Bank, in payment of any costs, charges, expenses and liabilities incurred by the Bank and every person appointed by the Bank under the Security Documents;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3* cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> THIRDLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in or towards payment to the Bank of all interest then accrued and remaining unpaid in respect of the Housing Loan;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> FOURTHLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in or towards payment to the Bank of the principal sum due and remaining unpaid under the Housing Loan;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> FIFTHLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in or towards payment to the Bank of all other moneys due and remaining unpaid under any or all of the Security Documents;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> SIXTHLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in or towards payment to the Bank of all other moneys due and remaining unpaid;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 10))
    ptext = "<font size=10> SEVENTHLY </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>any surplus will be paid to persons entitled to such surplus;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.3 * cm, 3.6 * cm, 10.3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext2 = '<font size=11>PROVIDED ALWAYS THAT the Bank may alter the above order of payment or keep such amounts in a non-interest bearing suspense account. Such alteration in the order of payment, or payment into a suspense account, will not affect the right of the Bank to receive the full amount to which it would have been entitled if the primary order had been observed, or any lesser amount which the sum ultimately realised from the security may be sufficient to pay.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=12>Section 9.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Deficiency in Proceeds of Sale</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>9.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The parties agree that, regardless of any other provision contained in this Agreement to the contrary:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (a) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>if the actual amount ultimately received by the Bank under the terms of the Security Documents and/or on a sale of the assets or properties charged and/or assigned to the Bank under the Security Documents, after deduction of all fees (including but not limited to the Bank’s solicitors fees on a solicitor and client basis), costs, rates, taxes and other outgoings on the assets or properties charged and/or assigned to the Bank under the Security Documents, is less than the amount due to the Bank under the Letter of Offer and this Agreement, the Borrower will be liable for the amount of such shortfall;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = "<font size=11> (b) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>paragraph (a) applies whether or not the Bank is the purchaser of all the assets or properties charged and/or assigned to the Bank under the Security Documents at such sale;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (c) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>until payment is made for the amount of the shortfall, the Borrower will (regardless of any foreclosure proceedings taken or sale made by the Bank) also pay interest (both before demand as well as after judgment and irrespective of whether or not the banker and customer relationship exists or has been terminated) on the shortfall at the Prescribed Rate and if applicable, the Default Rate, up to the date such shortfall together with all accrued interests is actually received in full by the Bank; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (d) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>any interest payable under this Section 9.3 is to be calculated and charged in accordance with Section 4.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=12><b>SECTION 10</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>Section 10.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Agreement to maintain Mortgage Insurance Policy</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>10.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>If the Borrower is required to take up, or in the event that the Bank takes up on the Borrower’s behalf, and maintains a mortgage reducing term policy, or any other policy, guaranteeing the repayment of the Indebtedness, the Borrower expressly agrees with the Bank to:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (a) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>cause the interest of the Bank as loss payee to be endorsed on the insurance policy so taken up;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (b) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>pay the premium on such policies; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (c) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>deliver the receipts for such payments to the Bank.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>Section 10.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Agreement to maintain insurance on the Property</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    index = "<font size=12>10.2</font>"
    index_1 = (Paragraph(index,styles['t1']))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=12>The Borrower expressly agrees with the Bank that whenever required by the Bank, the Borrower will:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[index_1, ptext_1, ptext_2,'']]
    t = Table(able, (2*cm, 1.5   * cm, 13 * cm,1*cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (a) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>ensure that the Property is adequately insured up to their full insurable value, against loss or damage by fire, lightning, tempest, flood, riot, civil commotion, malicious acts and strike and such other risks as the Bank may require, with a reputable insurance company approved by the Bank;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (b) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>ensure that the interest of the Bank as chargee or assignee and loss payee is endorsed on the insurance policy or policies so taken up; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (c) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>deposit with the Bank a certified true copy of the policy or policies so taken up together with evidence of payment of the current premium payable under such policy or policies.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>(ii)</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The Borrower also expressly agrees that the Bank may but is not obliged to insure and keep the Property insured in accordance with Section 10.2(i)(a). In the event the Bank proceeds to do so, the Borrower shall be required to pay the insurance premium on demand by the Bank. If the Borrower fails to pay the insurance premium, the Bank shall proceed to make the payment on behalf of the Borrower and such payment shall be added to the Indebtedness or the Housing Loan.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>Section 10.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Agreement to inform Bank change of address</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>10.3</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The Borrower expressly agrees with the Bank to inform the Bank immediately of any change in the correspondence address of the Borrower.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 11</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>11.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Notices by Bank</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext2 = '<font size=12>Notices may be given or made by post, facsimile, personal delivery or such other mode as may be practicable and allowed by the Bank. Notices issued by or on behalf of the Bank (including computer generated notices/ statements that do not require any signature) will be directed to the Borrower at the Borrower’s address, facsimile number or electronic mail address as stated in the Letter of Offer or the last known address, facsimile number or electronic mail address notified by the Borrower.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>11.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Deemed Delivery</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext2 = '<font size=12>The Notices are deemed delivered to the Borrower:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (i) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in the case of post, two (2) days after the date of posting, regardless of whether the Notices are returned undelivered or unclaimed;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (ii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in the case of facsimile, on the day of transmission;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (iii) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in the case of electronic mail, on the day of transmission provided that the Bank has not received a failed or undeliverable message from the host provider of the recipient within the day of transmission; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (iv) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>in the case of personal delivery, at the time of delivery.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (2.1 * cm, 2 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>PART B</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 12</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>FURTHER DEFINITIONS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>12.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>In Part B, the following words have the meaning given to them below.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><b>Authorised Persons</b> </font>"
    ptext_1 = (Paragraph(ptext, styles['Normal']))
    ptext2 = "<font size=10>any person the Borrower authorises (either alone or collectively), and approved by the Bank, to operate the Borrower’s account, and to act on the Borrower’s behalf in giving instructions, to perform any acts under an agreement between the Bank and the Borrower, or to use any facility, product or service the Bank makes available to the Borrower.<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11><b> Group</b> </font>"
    ptext_3 = (Paragraph(ptext3, styles['Normal']))
    ptext4 = "<font size=10>the Bank’s branches, agencies, representative offices, affiliated, associated or related corporations, and their respective officers, servants or agents, whether situated in or out of Malaysia, and includes the Bank.<br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['',ptext_1, ptext_2],['',ptext_3,ptext_4]]
    t = Table(able, (3*cm, 3.5 * cm, 9 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (1, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (1, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 13</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> REPRESENTATIONS AND WARRANTIES</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>13.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>By signing this Agreement, the Borrower makes the following representations and gives the following warranties to the Bank:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> 13.1.1 </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>that the Borrower has the power, right and capacity to execute, deliver and perform the terms of this Agreement and the Security Documents;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> 13.1.2 </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>that this Agreement and the Security Documents, when executed, will constitute legal, valid and binding obligations of the Borrower enforceable in accordance with their respective terms;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> 13.1.3 </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>that the execution, delivery and performance of this Agreement and the Security Documents:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> (a) </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>will not breach any law, regulation, order or decree of any governmental authority, agency or court to which the Borrower is/are subject; and</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> (b) </font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=10>will not breach any provision of any contract, mortgage, undertaking or instrument to which the Borrower is/are party or which is binding on them and will not result in the creation or imposition of any obligation to create or impose any mortgage, charge, lien, pledge or other security interest in the Property or in the Security Documents or on the assets or moneys of the Borrower;</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2],['',ptext_3,ptext_4]]
    t = Table(able, (2.5 * cm, 2 * cm, 10 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> 13.1.4 </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10>that all consents, licences, approvals, authorisations, orders and exemptions of any ministry, agency, department or authority in Malaysia and elsewhere which are required or advisable to be obtained in connection with the execution, delivery and performance, legality and enforceability of this Agreement and the Security Documents have been obtained and are in full force and effect and that no further consent, licence, approval, authorisation, order or exemption is required;<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 13.1.5 </font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=10>that the conditions contained in any consent, licence, approval, authorisation, order or exemption which are required or advisable to be obtained have been duly complied with;<br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11> 13.1.6 </font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=10>that there are no proceedings (whether civil or criminal), current or pending, before any court or before any government agency or administrative body or, to the knowledge of the Borrower, threatened against or affecting the Borrower;<br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11> 13.1.7 </font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=10>that the Borrower has not committed any act of bankruptcy and that no bankruptcy proceedings have been commenced or are being threatened against the Borrower;<br/><br/></font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9 = "<font size=11> 13.1.8 </font>"
    ptext_9 = (Paragraph(ptext9, styles['t1']))
    ptext10 = "<font size=10>that the Borrower has filed all tax returns which the Borrower is required by law to file and have paid or made adequate provision for the payment of all taxes, assessments, fees and other governmental charges assessed against the Borrower or upon the Borrower’s properties, assets, businesses or incomes;<br/><br/></font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    ptext11 = "<font size=11> 13.1.9 </font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12 = "<font size=10>that no Event of Default has occurred and is continuing;<br/><br/></font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    ptext13 = "<font size=11> 13.1.10 </font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14 = "<font size=10>that there has been no change in the financial condition of the Borrower which would materially affect in an adverse way the ability of the Borrower to perform the obligations of the Borrower under this Agreement and the Security Documents;<br/><br/></font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    ptext15 = "<font size=11> 13.1.11 </font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16 = "<font size=10>that all the information given by the Borrower to the Bank in connection with the Housing Loan do not contain any untrue or misleading statement or omit to state any fact and that all expressions of expectation, intention, belief and opinion and all projections contained in such information were honestly made on reasonable grounds after due and careful enquiry; and<br/><br/></font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    ptext17 = "<font size=11> 13.1.12 </font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18 = "<font size=10>that the Borrower is not aware of and has not intentionally withheld any information or fact which may result in or give rise to the offering or the grant of the Housing Loan by the Bank breaching any law or regulation including, without limitation, Section 62 of the Banking and Financial Institutions Act 1989, or any lending limits or restrictions that may be imposed upon the Bank from time to time by Bank Negara Malaysia or such other authority having jurisdiction over the Bank.<br/><br/></font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    able = [['', ptext_1, ptext_2],['',ptext_3,ptext_4],['',ptext_5,ptext_6],['',ptext_7,ptext_8],['',ptext_9,ptext_10],['',ptext_11,ptext_12],['',ptext_13,ptext_14],['',ptext_15,ptext_16],['',ptext_17,ptext_18]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>13.2</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The Borrower acknowledges that the Bank has entered into this Agreement on the basis of and in full reliance of the representations and warranties above and the Borrower agrees, covenants, undertakes and confirms that each of the representations and warranties above shall survive and continue to have full force and effect after the execution of this Agreement and the Security Documents and will be true and correct and fully observed on each and every date that the Housing Loan is utilised and until the Indebtedness has been fully and completely discharged.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>13.3</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4= "<font size=12>The Bank's rights and remedies in relation to any misrepresentation or breach of warranty shall not be affected in any way by any investigation by or on behalf of the Bank into the affairs of the Borrower, by the execution or the performance of this Agreement, or by any other act or thing which may be done by or on behalf of the Bank in connection with this Agreement or which might, apart from this Section, affect such rights or remedies.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext1, ptext_2],[ptext_3,ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 14</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> PURPOSE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>14.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>If the Letter of Offer sets out a purpose for the Housing Loan, the Borrower must use the Housing Loan only for such purpose; the Bank may, in its sole discretion and in writing, allow the Housing Loan to be used for another purpose.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>14.2</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=12>Without in any way affecting the Borrower’s obligation in Section 14.1, the Bank need not check or concern itself with how the Borrower actually uses the Housing Loan.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext1, ptext_2], [ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 15</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> NO OBLIGATION TO ADVANCE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>15.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>The Bank has no obligation whatsoever to make or to continue to make available the Housing Loan or any part of it to the Borrower or to make or to continue to make any advance of the Housing Loan; nothing in this Agreement shall be read to mean that the Bank has such an obligation whether in law or in equity.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12>15.2</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=12>Regardless of whatever else may be contained in this Agreement, the Borrower expressly understands and agrees that the Housing Loan may be reviewed at any time and from time to time by the Bank.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12>15.3</font>'
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=12>Upon any review of the Housing Loan by the Bank, the Bank may impose such terms and conditions as the Bank deems fit including, without limitation, reducing the principal amount of the Housing Loan or requiring payment and repayment of any Indebtedness.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext1, ptext_2], [ptext_3, ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 16</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> CONDITIONS PRECEDENT</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>16.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>Subject to the terms and conditions contained in this Agreement, the Housing Loan will be available for utilisation by the Borrower only upon the satisfaction or fulfillment of the following conditions precedent:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> 16.1.1 </font>"
    ptext_1 = (Paragraph(ptext, styles['t1']))
    ptext2 = "<font size=10><u>Execution</u><br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    content1 = "<font size=10>This Agreement and the Security Documents must have been duly executed, stamped and registered with such registries as the Bank may consider necessary and copies of those documents must have been delivered to the Bank.</font>"
    content_1 = (Paragraph(content1,styles['Justify']))
    ptext3 = "<font size=11> 16.1.2 </font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=10><u>Bankruptcy Search</u><br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    content2 = "<font size=10>The Bank must have received from the Director General of Insolvency, Malaysia, or, if the Borrower is not a citizen of Malaysia, the relevant registry of the country of citizenship, the results of the searches made on the Borrower confirming that the Borrower has not been adjudged bankrupt and that no petition or order for the bankruptcy of the Borrower has been made or received against the Borrower.</font>"
    content_2 = (Paragraph(content2, styles['Justify']))
    ptext5 = "<font size=11> 16.1.3 </font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=10><u>No Misrepresentation or Breach of Warranty</u><br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    content3 = "<font size=10>There must not have occurred any misrepresentation or breach of any of the warranties contained in this Agreement.</font>"
    content_3 = (Paragraph(content3, styles['Justify']))
    ptext7 = "<font size=11> 16.1.4 </font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=10><u>Payment of Fees, Costs and Expenses</u><br/><br/></font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    content4 = "<font size=10>All fees, costs and expenses which are due and payable or which have accrued by virtue of this Agreement or any Security Document must have been fully paid and settled.</font>"
    content_4 = (Paragraph(content4, styles['Justify']))
    ptext9 = "<font size=11> 16.1.5 </font>"
    ptext_9 = (Paragraph(ptext9, styles['t1']))
    ptext10 =  "<font size=10><u>No Event of Default</u><br/><br/></font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    content5 = "<font size=10>No Event of Default as set out in this Agreement and no event which, with the giving of notice or lapse of time or both, would constitute such an Event of Default must have occurred and/or is continuing.</font>"
    content_5 = (Paragraph(content5, styles['Justify']))
    ptext11 = "<font size=11> 16.1.6 </font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12 = "<font size=10><u>Receipt of Additional Documents, etc</u><br/><br/></font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    content6 = "<font size=10>The Bank must have received such other documents, undertakings, confirmations, opinions, certificates, authorisations or assurances as the Bank may in its sole discretion consider necessary.</font>"
    content_6 = (Paragraph(content6, styles['Justify']))
    ptext13 = "<font size=11> 16.1.7 </font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14 ="<font size=10><u>No Change in Ability to Perform</u><br/><br/></font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    content7 = "<font size=10>There must not have occurred any extraordinary circumstance, change of law or change in the financial position of the Borrower which, in the sole opinion of the Bank, would affect or prejudice the ability of the Borrower to fully perform and discharge its respective obligations under this Agreement or the Security Documents.</font>"
    content_7 = (Paragraph(content7, styles['Justify']))
    ptext15 = "<font size=11> 16.1.8 </font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16 =  "<font size=10><u>No change in Financial, Economic or Political Situation</u><br/><br/></font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    content8 = "<font size=10>There must not have occurred any change in the financial, economic or political conditions in Malaysia which, in the sole opinion of the Bank, would make it inadvisable or impractical for the Bank to make or to continue to make available the Housing Loan or any utilisation of the Housing Loan.</font>"
    content_8 = (Paragraph(content8, styles['Justify']))
    ptext17 = "<font size=11> 16.1.9 </font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18 = "<font size=10><u>Compliance with Operational Requirements</u><br/><br/></font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    content9 = "<font size=10>The Borrower must have complied with all the Bank's operational requirements to the satisfaction of the Bank.</font>"
    content_9 = (Paragraph(content9, styles['Justify']))
    ptext19 = "<font size=11> 16.1.10 </font>"
    ptext_19 = (Paragraph(ptext19, styles['t1']))
    ptext20 = "<font size=10><u>Compliance with Additional and/or Other Conditions Precedent</u><br/><br/></font>"
    ptext_20 = (Paragraph(ptext20, styles['Justify']))
    content10 = "<font size=10>If additional and/or other conditions precedent are set out in the Letter of Offer, the Borrower must have complied with such additional and/or other conditions precedent.</font>"
    content_10 = (Paragraph(content10, styles['Justify']))
    able = [['', ptext_1, ptext_2],['','',content_1], ['', ptext_3, ptext_4],['','',content_2], ['', ptext_5, ptext_6],['','',content_3], ['', ptext_7, ptext_8],['','',content_4],
            ['', ptext_9, ptext_10],['','',content_5], ['', ptext_11, ptext_12],['','',content_6], ['', ptext_13, ptext_14],['','',content_7], ['', ptext_15, ptext_16],['','',content_8],
            ['', ptext_17, ptext_18],['','',content_9],['',ptext_19,ptext_20],['','',content_10]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 17</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> PAYMENTS AND REPAYMENTS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12>17.1</font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12>All moneys to be paid or repaid to the Bank under this Agreement and the Security Documents must be paid:-</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1 = "<font size=11> 17.1.1 </font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>unconditionally and free of any restriction of any kind; and<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 17.1.2 </font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>without any deduction of any kind including, without limitation, deductions for any bank charges or commissions, any kind of withholding tax, and any set-off or counterclaim claimed against the Bank.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = '<font size=12>17.2</font>'
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2 = '<font size=12>If any applicable law requires that there has to be a deduction or withholding from the moneys to be paid or repaid to the Bank under this Agreement and the Security Documents, the Borrower shall pay such additional sum as would be necessary to ensure that, after the making of the deduction or withholding, the Bank will have received on the due date a net amount equal to what the Bank would have received and been entitled to retain had no such deduction or withholding been required.</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = '<font size=12><br/>17.3</font>'
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = '<font size=12><br/>Without in any way affecting any of the provisions in this Agreement, if any kind of goods and services tax or any tax, charge or levy of a similar nature is required by any law to be paid in respect of any moneys payable or repayable to the Bank under this Agreement or the Security Documents, such tax, charge or levy shall be included in the Indebtedness and shall be paid by the Borrower.</font>'
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = '<font size=12><br/>17.4</font>'
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = '<font size=12><br/>All payments to be made by the Borrower under this Agreement shall be made in Ringgit Malaysia in immediately available funds on the due dates at the place of business of the Bank set out in Section 2 of the Schedule or at any other address which the Bank may specify from time to time. However, for a Housing Loan in foreign currencies, payments may be made in the currencies in which the Housing Loan was provided.</font>'
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = '<font size=12><br/>17.5</font>'
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    ptext8 = '<font size=12><br/>If any moneys are due to be paid or repaid to the Bank on a day which is not a Banking Day, the payment or repayment shall be made on the Banking Day immediately following that day; if the Banking Day immediately following that day falls in a different calendar month, the payment or repayment shall be made on the Banking Day immediately before that day.</font>'
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6],[ptext_7,ptext_8]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 18</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> CONTINUING SECURITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext3 = "<font size=11><br/>18.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>This Agreement is and will be a continuing security for the Indebtedness, and will continue to be held by the Bank until –</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3,ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> (a)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>all amounts outstanding under the Housing Loan, including contingent liabilities, have been fully settled by the Borrower; and<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> (b)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>the Bank has been fully released from all its obligations or contingent liabilities under the Housing Loan or under any other instrument issued by the Bank for the account of the Borrower,</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext2 = '<font size=11>even if the Borrower ceases to be indebted to the Bank for any period(s), and regardless of –</font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> (c)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>any account(s) ceasing to be current or any settlement or closure of account(s) or otherwise; or<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> (d)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>the death, insanity or bankruptcy of the Borrower.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>SECTION 19</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>FURTHER ASSURANCE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext3 = "<font size=11><br/>19.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>The Borrower will, whenever required by the Bank, at the Borrower’s own cost and expense make, sign, do and perform and cause to be made, signed, done and performed all such further acts, agreements, assignments, assurances, deeds, mortgages, charges and documents of any nature as reasonably required to perfect the security created or intended to be created under this Agreement and the Security Documents.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 20</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> SECURITY MARGIN</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext3 = "<font size=11><br/>20.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>If the market value of the Property falls below what the Bank in the Bank’s sole discretion considers to be adequate security for the Housing Loan, the Bank may do any one or more of the following without affecting any other right which the Bank may have:-</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> 20.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>reduce the credit limit of the Housing Loan;<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 20.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>withhold further release or utilisation of any part of the Housing Loan;</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11> 20.1.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=11>require the Borrower to make repayment of such amount of the Housing Loan as the Bank may decide upon;</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11> 20.1.4</font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=11>require the Borrower to make prepayment of the Housing Loan in which case the Bank will not charge the Borrower any prepayment fee; and/or</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9  = "<font size=11> 20.1.5</font>"
    ptext_9 = (Paragraph(ptext9, styles['t1']))
    ptext10 = "<font size=11>require additional security acceptable to the Bank to be provided for the Housing Loan.</font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4],['', ptext_5, ptext_6],['', ptext_7, ptext_8],['', ptext_9, ptext_10]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 21</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> CONCURRENT PROCEEDINGS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext3 = "<font size=11><br/>21.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>The Borrower agrees that the obligations to pay and repay the Bank under this Agreement and the Security Documents are separate and independent obligations which give the Bank separate and independent rights and causes of action regardless of any waiver or indulgence which may have been granted by the Bank in respect of any one or more of those obligations; accordingly, the Bank shall have the right to seek remedy in respect of a breach of any one of those obligations independently of or at the same time as any other remedy the Bank may seek in respect of any other breach of those obligations. In particular, the Bank shall have the right to commence any action in respect of any breach of those obligations without having first resorted to any other remedy or having first sold or disposed of the Property.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>SECTION 22</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>BORROWING AND CHARGING POWERS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext3 = "<font size=11><br/>22.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>Where any moneys are owing and secured by any Security Document, they will be deemed to be so owing and secured regardless of:-</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> 22.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>any legal limitation, incapacity or otherwise of the Borrower in respect of the borrowing of the Housing Loan which might be a defence as between the Borrower and the Bank;<br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 22.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>the Borrower’s power to enter into the Security Document; or</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11> 22.1.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=11>any legal limitation in the power of any attorney, agent or other person purporting to act or acting on behalf of the Borrower or any other irregularity in the borrowing or incurring of the liabilities.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4],['',ptext_5,ptext_6]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 23</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> AVOIDANCE OF SECURITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext3 = "<font size=11><br/>23.1</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>The Bank's rights to recover from the Borrower the whole of the Indebtedness shall not be affected in any way whatsoever:-</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_3, ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> 23.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>by any assurance, security or payment which may be avoided under any law relating to winding-up or insolvency; and<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 23.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>by any release, settlement or discharge given or made by the Bank on the basis of such assurance, security or payment;</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11><br/>any such release, settlement or discharge shall be taken to have been made on the condition that it will be void if any payment or security which the Bank may previously have received or may receive after this Agreement in respect of the Indebtedness is set aside under any applicable law or is found to be not valid for any reason whatsoever.</font>"
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    able = [['', ptext_1]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 24</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>ASSIGNMENT / TRANSFER OF SECURITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11><br/>24.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2 = "<font size=11><br/>The Bank can, at any time at its sole discretion and without notifying the Borrower, assign or transfer all or any part of its rights, interests, benefits and obligations under this Agreement and/or any Security Document.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11><br/>24.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11><br/>The costs and expenses of the Bank and the assignee or transferee are to be paid by the Borrower.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11><br/>24.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11><br/>Following any such assignment or transfer, the assignee or transferee will assume and be entitled to the rights, interests, benefits and obligations of this Agreement and/or the Security Document as if the assignee or transferee had been a party to this Agreement and/or the Security Document in place of the Bank.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5, ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>SECTION 25</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>INDEMNITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1  = "<font size=11><br/>25.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2  = "<font size=11><br/>In addition and without affecting the powers, rights, and remedies granted under this Agreement, the Borrower will indemnify the Bank against any loss or expenses (including legal expenses on a solicitor and client basis) which the Bank sustains or incurs because of –</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11> (a)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2  = "<font size=11>any cancellation or failure of the Borrower to draw the whole or any part of the Housing Loan; or<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3  = "<font size=11> (b)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4  = "<font size=11>any prepayment of the Housing Loan or any part of it unless otherwise provided under this Agreement or the Letter of Offer; or</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5  = "<font size=11> (c)</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6  = "<font size=11>any default in payment by the Borrower of any sum due under this Agreement, including any interest or fees paid or payable on account of, or in respect of, any funds borrowed or deposits from third parties in order to maintain the amount in default, or in liquidating or re-employing such funds or deposits; or<br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7  = "<font size=11> (d)</font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8  = "<font size=11>the occurrence of any Event of Default.</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able    = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4],['',ptext_5,ptext_6],['',ptext_7,ptext_8]]
    t       = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11><br/>25.2</font>"
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2  = "<font size=11><br/>The Bank’s certification of the amount of the said loss or expenses will be conclusive and binding upon the Borrower unless there is any obvious mistake.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext_1, ptext_2]]
    t       = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext   = '<font size=12><b>SECTION 27</b></font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12><b>RIGHT TO DEBIT</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)

    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11><br/>27.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['Justify']))
    ptext2  = "<font size=11><br/>Without affecting any other rights that the Bank may have under this Agreement or by law, the Bank may, at any time, at the Bank’s sole discretion, and without giving the Borrower any prior notice, debit the Borrower’s current account or any other account (including the balance on any overdraft account) which the Borrower may have with the Bank whether alone or with any other person with any moneys whatsoever which are payable by the Borrower to the Bank.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3  = "<font size=11>27.2</font>"
    ptext_3 = (Paragraph(ptext3,styles['Justify']))
    ptext4  = "<font size=11>If the Bank does debit the Borrower’s account, the debiting is not to be taken as a waiver of any of the Events of Default listed in this Agreement.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5  = "<font size=11>27.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6  = "<font size=11>If any debiting of any of the Borrower’s accounts causes that account to be overdrawn, interest at the default rate shall be payable to the Bank accordingly.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able    = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6]]
    t       = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext   = '<font size=12><b>SECTION 28</b></font>'
    ptext1  = (Paragraph(ptext, styles['Justify']))
    ptext2  = '<font size=12><b>RIGHT OF SET-OFF</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able    = [[ptext1, ptext_2]]
    t       = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext   = "<font size=11>28.1</font>"
    ptext_1 = (Paragraph(ptext,styles['Justify']))
    ptext2  = "<font size=11>The Borrower agrees that the Bank has the right, without any notice to the Borrower, to combine, consolidate or merge all or any of the Borrower’s accounts and liabilities with and to the Bank whether singly or jointly with any other person. The Bank also has the right, after giving the Borrower seven (7) days’ notice, to transfer or set off any sums in credit in such accounts in or towards the satisfaction of any of the Indebtedness, whether actual or dependent upon the occurrence of an event, primary or collateral, or joint or several.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3  = "<font size=11>28.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4  = "<font size=11>If any of the Indebtedness is dependent upon the occurrence of an event, the Bank has the right to set-off and transfer any sum standing to the credit of any of the Borrower’s accounts which the Borrower may have with the Bank whether alone or with any other person towards satisfaction of the Indebtedness and if the Indebtedness is less than the amount set-off by the Bank, the Bank will refund the surplus accordingly.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5  = "<font size=11>28.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6  = "<font size=11>If any of the Borrower’s accounts in credit is maintained in a currency other than the currency of the Indebtedness, the Bank may convert them into the currency of the Indebtedness at the Bank’s own prevailing rate.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7  = "<font size=11>28.4</font>"
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    ptext8  = "<font size=11>Upon the issuance of the notice mentioned in Section 28.1, the Borrower agrees that the Bank has the right to earmark or to place a hold on any monies standing to the credit of all or any of the Borrower’s accounts with the Bank prior to the setting-off, and the Borrower shall not be entitled to withdraw the monies without the Bank’s prior written consent.</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able    = [[ptext_1, ptext_2], [ptext_3, ptext_4], [ptext_5, ptext_6],[ptext_7,ptext_8]]
    t       = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 29</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>SUSPENSE ACCOUNT AND PROOF OF DEBT</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>29.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Bank can place and keep any money paid to it under this Agreement or any Security Document in a non-interest bearing suspense account for as long as the Bank thinks fit, without being obliged to use any part of it towards discharging any liability due or incurred by the Borrower.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>29.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>Regardless of the payment of any such money, if the Borrower becomes the subject of any bankruptcy, insolvency or similar proceedings, the Bank may prove for and agree to accept any dividend or composition in respect of the whole or any part of such money.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>29.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>After the Bank has received the ultimate balance in full, any claim on the part of the Borrower to any excess or any security remaining with the Bank will be a matter of adjustment between the Bank and the Borrower and/or any other person or persons laying claim to the same.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_1, ptext_2], [ptext_3, ptext_4], [ptext_5, ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 30</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>CHANGE IN THE BANK</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext = "<font size=11>30.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The security, liabilities, and/or obligations created by this Agreement or any Security Document will continue to be valid and binding for all purposes, regardless of any transfer or assignment of the Bank’s business, operations, assets, or liabilities, or any change by amalgamation, consolidation, reconstruction, or otherwise in the Bank’s constitution, or of any company by which the Bank’s business is carried on, and will be available by the company carrying on that business.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 31</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>MODIFICATION AND INDULGENCE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>31.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Bank may at any time and without in any way affecting the security created under this Agreement and the Security Documents:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext1   = "<font size=11> 31.1.1</font>"
    ptext_1  = (Paragraph(ptext1, styles['t1']))
    ptext2   = "<font size=11>terminate, vary or increase the amount of the Housing Loan or any part of the Housing Loan or any credit or other facility granted to the Borrower and may open and/or continue any account or accounts whatsoever with the Borrower at any office of the Bank;<br/><br/></font>"
    ptext_2  = (Paragraph(ptext2, styles['Justify']))
    ptext3   = "<font size=11> 31.1.2</font>"
    ptext_3  = (Paragraph(ptext3, styles['t1']))
    ptext4   = "<font size=11>in addition to and without in any way affecting the Bank's right of review under this Agreement vary or not comply with the provisions of this Agreement and/or the Security Documents and the Borrower expressly consents to any such variation and/or non-compliance;</font>"
    ptext_4  = (Paragraph(ptext4, styles['Justify']))
    ptext5   = "<font size=11>31.1.3</font>"
    ptext_5  = (Paragraph(ptext5,styles['t1']))
    ptext6   = "<font size=11>grant to the Borrower or any other person any time or indulgence;</font>"
    ptext_6  = (Paragraph(ptext6, styles['Justify']))
    ptext7   = "<font size=11>31.1.4</font>"
    ptext_7  = (Paragraph(ptext7, styles['t1']))
    ptext8   = "<font size=11>renew any bills, notes or other negotiable securities;</font>"
    ptext_8  = (Paragraph(ptext8, styles['Justify']))
    ptext9   = "<font size=11>31.1.5</font>"
    ptext_9  = (Paragraph(ptext9, styles['t1']))
    ptext10  = "<font size=11>deal with, exchange, release or modify or abstain from perfecting or enforcing any Security Document or rights the Bank may now or at any time after this Agreement have against the Borrower or any other person;</font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    ptext11  = "<font size=11>31.1.6</font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12  = "<font size=11>enter into any arrangement whatsoever with the Borrower or any other person;</font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    ptext13  = "<font size=11>31.1.7</font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14  = "<font size=11>at the request of the Borrower accept payment or repayment of any amounts due or becoming due under this Agreement and/or any Security Document by such increased or reduced instalments as the Bank may agree to;</font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    ptext15  = "<font size=11>31.1.8</font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16  = "<font size=11>at the request of the Borrower agree to suspend payments to reduce any principal repayable to the Bank under this Agreement and/or any Security Document;</font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    ptext17  = "<font size=11>31.1.9</font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18  = "<font size=11>grant further or other banking facilities to the Borrower;</font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    ptext19  = "<font size=11>31.1.10</font>"
    ptext_19 = (Paragraph(ptext19, styles['t1']))
    ptext20  = "<font size=11>reinstate, change, interchange, substitute or convert any of the banking facilities granted by the Bank to the Borrower, including, for the avoidance of doubt, the Housing Loan;</font>"
    ptext_20 = (Paragraph(ptext20, styles['Justify']))
    ptext21  = "<font size=11>31.1.11</font>"
    ptext_21 = (Paragraph(ptext21, styles['t1']))
    ptext22  = "<font size=11>reinstate, change, interchange, substitute or convert the principal limits or sub-principal limits of any of the banking facilities granted by the Bank to the Borrower including, for the avoidance of doubt, the Housing Loan; and/or</font>"
    ptext_22 = (Paragraph(ptext22, styles['Justify']))
    ptext23  = "<font size=11>31.1.12</font>"
    ptext_23 = (Paragraph(ptext23,styles['t1']))
    ptext24  = "<font size=11>for the purpose of recovering the Indebtedness, resort to all or any of the remedies or means set out in this Agreement and/or any Security Document at any time and in such order or sequence as the Bank may in its sole discretion think fit.</font>"
    ptext_24 = (Paragraph(ptext24, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4],['', ptext_5, ptext_6],
            ['', ptext_7, ptext_8],['', ptext_9, ptext_10],['', ptext_11, ptext_12],
            ['', ptext_13, ptext_14],['', ptext_15, ptext_16],['', ptext_17, ptext_18],
            ['', ptext_19, ptext_20],['', ptext_21, ptext_22],['', ptext_23, ptext_24]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>31.2</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>If the Bank at any time and from time to time in its sole discretion, grant additional or further banking facilities or vary or substitute the Housing Loan (or any of them if more than one) with any other banking facility upon such terms and conditions as may be prescribed by the Bank, all the provisions of this Agreement and the Security Documents, except for those provisions which are inconsistent with the terms and conditions prescribed by the Bank for the additional or further banking facilities or varied or substituted Housing Loan, shall continue to apply unless otherwise stated by the Bank.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>SECTION 32</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> VARIATION</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>32.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower acknowledges and the Borrower agrees that the provisions of this Agreement and the Security Documents, and the availability, limits, interest rates, commission, fees and charges of and relating to the Housing Loan are subject to:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1 = "<font size=11> 32.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>guidelines issued from time to time by Bank Negara Malaysia or any other authority having jurisdiction over the Bank; and<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 32.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>the Bank’s review and variation from time to time at the Bank’s sole discretion.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>32.2</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>If there is a change in any fees and charges, the Bank will give the Borrower twenty-one (21) days’ prior notice before the change takes effect.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext = '<font size=12><b>SECTION 33</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b> NON-UTILISATION OF FACILITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>33.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>If the Letter of Offer prescribes a time period during which the Housing Loan must be fully or partly utilised, and if the Housing Loan is not fully or partly utilised during that time period, the Bank may in its sole discretion withdraw the Housing Loan or any unutilised portion of the Housing Loan; if the Bank does withdraw the Housing Loan or any unutilised portion of the Housing Loan:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11> 33.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>the Borrower must still pay to the Bank all the fees, costs and expenses which may have been incurred by the Bank; and/or<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11> 33.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>the Bank may vary the Housing Loan and impose new terms and conditions.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 34</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>CESSATION OF RELATIONSHIP</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>34.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The cessation of the banker-customer relationship between the Bank and the Borrower will not in any circumstances or in any manner affect the Bank’s right to capitalize any interest payable on any outstanding balance.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 35</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>CERTIFICATE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>35.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>Any certificate or statement issued by the Bank showing the outstanding amount due and owing from the Borrower to the Bank in relation to the Housing Loan will be conclusive proof as to the outstanding amount due and owing from the Borrower to the Bank in relation to the Housing Loan; this certificate or statement will be binding on the Borrower for all purposes whatsoever including for the purposes of any legal proceedings.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 36</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>DISCLOSURE OF INFORMATION</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>36.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower agrees that the Bank (including the Bank’s officers, employees, agents or any other persons to whom the Bank may grant access to the Borrower’s records, correspondence or any material relating to the Borrower or the Borrower’s account) can disclose at any time at the Bank’s sole discretion without notifying the Borrower beforehand, any information relating to the Borrower, the Borrower’s account and any of the Borrower’s Authorised Persons to the following:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1 = "<font size=11> 36.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>any one or more members of the Group for any of the following purposes:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [['', ptext_1, ptext_2]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1 = "<font size=11>(a)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>providing the Borrower with banking services;<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>(b)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>reporting;<br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>(c)</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=11>data matching;<br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11>(d)</font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=11>improving and furthering the provision of other services by the Bank;<br/><br/></font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9 = "<font size=11>(e)</font>"
    ptext_9 = (Paragraph(ptext9, styles['t1']))
    ptext10 = "<font size=11>fraud or crime prevention;<br/><br/></font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    ptext11 = "<font size=11>(f)</font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12 = "<font size=11>investigating, preventing or otherwise in relation to money laundering or any other criminal activities;<br/><br/></font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    ptext13 = "<font size=11>(g)</font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14 = "<font size=11>debt collection;<br/><br/></font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    ptext15 = "<font size=11>(h)</font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16 = "<font size=11>outsourcing the Bank’s operations or any part of the Bank’s operations;<br/><br/></font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    ptext17 = "<font size=11>(i)</font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18 = "<font size=11>performance of duties as an officer of the Bank or in connection with the conduct of audit or the performance of risk management;<br/><br/></font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    ptext19 = "<font size=11>(j)</font>"
    ptext_19 = (Paragraph(ptext19, styles['t1']))
    ptext20 = "<font size=11>facilitating the performance of the Bank’s or any member of the Group’s functions;<br/><br/></font>"
    ptext_20 = (Paragraph(ptext20, styles['Justify']))
    ptext21 = "<font size=11>(k)</font>"
    ptext_21 = (Paragraph(ptext21, styles['t1']))
    ptext22 = "<font size=11>compliance with the Group’s policies, guidelines, directives or requirements;<br/><br/></font>"
    ptext_22 = (Paragraph(ptext22, styles['Justify']))
    ptext23 = "<font size=11>(l)</font>"
    ptext_23 = (Paragraph(ptext23, styles['t1']))
    ptext24 = "<font size=11>corporate exercise;<br/><br/></font>"
    ptext_24 = (Paragraph(ptext24, styles['Justify']))
    ptext25 = "<font size=11>(m)</font>"
    ptext_25 = (Paragraph(ptext25, styles['t1']))
    ptext26 = "<font size=11>any legal process initiated by or served on the Bank;<br/><br/></font>"
    ptext_26 = (Paragraph(ptext26, styles['Justify']))
    able = [['', ptext_1, ptext_2],['', ptext_3, ptext_4],['', ptext_5, ptext_6],
            ['', ptext_7, ptext_8],['', ptext_9, ptext_10],['', ptext_11, ptext_12],
            ['', ptext_13, ptext_14],['', ptext_15, ptext_16],['', ptext_17, ptext_18],
            ['', ptext_19, ptext_20],['', ptext_21, ptext_22],['', ptext_23, ptext_24],
            ['', ptext_25, ptext_26]]
    t = Table(able, (1.3 * cm, 2 * cm, 9 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1   = "<font size=11> 36.1.2</font>"
    ptext_1  = (Paragraph(ptext1, styles['t1']))
    ptext2   = "<font size=11>any person, whether in Malaysia or elsewhere, who provides electronic or other services to the Bank for the purpose of providing, updating, maintaining and upgrading the services including, but not limited to, investigating discrepancies, errors or claims;<br/><br/></font>"
    ptext_2  = (Paragraph(ptext2, styles['Justify']))
    ptext3   = "<font size=11>36.1.3</font>"
    ptext_3  = (Paragraph(ptext3, styles['t1']))
    ptext4   = "<font size=11>any person, whether in Malaysia or elsewhere, engaged by the Bank in connection with the performance of services or operational functions which have been out-sourced;<br/><br/></font>"
    ptext_4  = (Paragraph(ptext4, styles['Justify']))
    ptext5   = "<font size=11>36.1.4</font>"
    ptext_5  = (Paragraph(ptext5, styles['t1']))
    ptext6   = "<font size=11>the police or any public officer conducting an investigation in connection with any offence including suspected offences;<br/><br/></font>"
    ptext_6  = (Paragraph(ptext6, styles['Justify']))
    ptext7   = "<font size=11>36.1.5</font>"
    ptext_7  = (Paragraph(ptext7, styles['t1']))
    ptext8   = "<font size=11>credit card companies and financial institutions in connection with credit card enquiries;<br/><br/></font>"
    ptext_8  = (Paragraph(ptext8, styles['Justify']))
    ptext9   = "<font size=11>36.1.6</font>"
    ptext_9  = (Paragraph(ptext9, styles['t1']))
    ptext10  = "<font size=11>other banks, financial institutions, credit bureau or credit reference agents (only for credit information);<br/><br/></font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    ptext11  = "<font size=11>36.1.7</font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12  = "<font size=11>the Bank’s auditors, solicitors, and professional advisors;<br/><br/></font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    ptext13  = "<font size=11>36.1.8</font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14  = "<font size=11>the Bank’s stationery printers, vendors of the computer systems the Bank uses, and to such persons installing and maintaining them and other suppliers of goods or service providers the Bank may engage;<br/><br/></font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    ptext15  = "<font size=11>36.1.9</font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16  = "<font size=11>any receiver appointed by the Bank or by any other party;<br/><br/></font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    ptext17  = "<font size=11>36.1.10</font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18  = "<font size=11>any credit bureau of which the Bank is a member, and any other members and/or compliance committee of such credit bureau;<br/><br/></font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    ptext19  = "<font size=11>36.1.11</font>"
    ptext_19 = (Paragraph(ptext19, styles['t1']))
    ptext20  =  "<font size=11>any rating agency, insurer or insurance broker or direct or indirect provider of credit protection;<br/><br/></font>"
    ptext_20 = (Paragraph(ptext20, styles['Justify']))
    ptext21  = "<font size=11>36.1.12</font>"
    ptext_21 = (Paragraph(ptext21, styles['t1']))
    ptext22  = "<font size=11>any actual or potential participant or sub-participant in relation to any of the Bank’s obligations under the banking agreement between the Bank and the Borrower, or assignee, novatee or transferee (or any officer, employee, agent or adviser) of any of them;<br/><br/></font>"
    ptext_22 = (Paragraph(ptext22, styles['Justify']))
    ptext23  = "<font size=11>36.1.13</font>"
    ptext_23 = (Paragraph(ptext23, styles['t1']))
    ptext24  = "<font size=11>for transactions effected or processed with or without the Borrower’s authority in or through the automated teller machines of other banks or financial or non-financial institutions or terminals or other card operated machines or devices the Bank approves, to the bank, financial institution or non-financial institution, trader or other party accepting the use of the automated teller machine card and their respective agents or contractors;<br/><br/></font>"
    ptext_24 = (Paragraph(ptext24, styles['Justify']))
    ptext25  = "<font size=11>36.1.14</font>"
    ptext_25 = (Paragraph(ptext25, styles['t1']))
    ptext26  = "<font size=11>any court, tribunal or authority, whether governmental or quasi- governmental with jurisdiction over the Bank or any member of the Group;<br/><br/></font>"
    ptext_26 = (Paragraph(ptext26, styles['Justify']))
    ptext27  = "<font size=11>36.1.15</font>"
    ptext_27 = (Paragraph(ptext27, styles['t1']))
    ptext28  = "<font size=11>any person to whom the Bank, or any member of the Group, is permitted or required to disclose to under the laws of any country;<br/><br/></font>"
    ptext_28 = (Paragraph(ptext28, styles['Justify']))
    ptext29  = "<font size=11>36.1.16</font>"
    ptext_29 = (Paragraph(ptext29, styles['t1']))
    ptext30  = "<font size=11>any other person to whom such disclosure is considered by the Bank to be in the Bank’s interest, or the interest of any members of the Group (not applicable to strategic alliance for marketing and promotional purpose);<br/><br/></font>"
    ptext_30 = (Paragraph(ptext30, styles['Justify']))
    ptext31  = "<font size=11>36.1.17</font>"
    ptext_31 = (Paragraph(ptext31, styles['t1']))
    ptext32  = "<font size=11>any person intending to settle any moneys outstanding under the Housing Loan;<br/><br/><br/><br/></font>"
    ptext_32 = (Paragraph(ptext32, styles['Justify']))
    ptext33  = "<font size=11>36.1.18</font>"
    ptext_33 = (Paragraph(ptext33, styles['t1']))
    ptext34  = "<font size=11>any person connected to the enforcement or preservation of any of the Bank’s rights under this Agreement and the Security Documents;<br/><br/></font>"
    ptext_34 = (Paragraph(ptext34, styles['Justify']))
    ptext35  = "<font size=11>36.1.19</font>"
    ptext_35 = (Paragraph(ptext35, styles['t1']))
    ptext36  = "<font size=11>the Central Credit Bureau or any other authority or body established by Bank Negara Malaysia or any other authority having jurisdiction over the Bank; and<br/><br/></font>"
    ptext_36 = (Paragraph(ptext36, styles['Justify']))
    ptext37  = "<font size=11>36.1.20</font>"
    ptext_37 = (Paragraph(ptext37, styles['t1']))
    ptext38  = "<font size=11>any security party.<br/><br/></font>"
    ptext_38 = (Paragraph(ptext38, styles['Justify']))
    able = [['', ptext_1, ptext_2],['', ptext_3, ptext_4],['', ptext_5, ptext_6],
            ['', ptext_7, ptext_8],['', ptext_9, ptext_10],['', ptext_11, ptext_12],
            ['', ptext_13, ptext_14],['', ptext_15, ptext_16],['', ptext_17, ptext_18],
            ['', ptext_19, ptext_20],['', ptext_21, ptext_22],['', ptext_23, ptext_24],
            ['', ptext_25, ptext_26],['', ptext_27, ptext_28],['', ptext_29, ptext_30],
            ['', ptext_31, ptext_32],['', ptext_33, ptext_34],['', ptext_35, ptext_36],
            ['', ptext_37, ptext_38]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 37</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>COMPLIANCE WITH COURT ORDERS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>37.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower agrees that the Bank and the Group can act in any way the Bank sees fit, without consulting the Borrower beforehand, if the Bank is served with a court order issued by a court of any jurisdiction. The Borrower agrees that the Borrower will not hold the Bank liable for any loss or damage in connection with the Bank’s actions.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 38</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>TIME OF THE ESSENCE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>39.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>Time, wherever referred to in this Agreement, shall be of the essence of this Agreement.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 40</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>BANK’S RIGHT TO MAKE ADJUSTMENTS</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>40.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Bank has the right to adjust the entries in its records or the account statement if there is any error or missing entries.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 41</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>SEARCHES</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>41.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Bank may but is not obliged to conduct bankruptcy/winding up searches or credit related searches from any credit reference agencies, database or system on any person before and at any time after the disbursement of any of the Housing Loan.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>41.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>The Borrower consents, and will procure the consent of each security party, to the Bank to carry out such searches on the Borrower and/or such security party to the extent permitted by the law.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>41.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>All charges incurred in connection with the above searches will be borne by the Borrower.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 42</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>DATA PROTECTION</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>42.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower agrees that the Group is permitted to process the Borrower’s Personal Data. For the purpose of this Agreement, the term “process”, “processing” and “processed” shall include but not limited to, collecting, recording, holding, storing or using.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>42.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>“Personal Data” may include, but is not limited to, the Borrower’s name, date of birth, identification card (NRIC), sex, marital status, race, current residential address, home number, office number, mobile number, email address, credit card details, name of employer, name of business owned by the Borrower, occupation, mother’s maiden name, highest educational qualification, annual income, the Borrower’s user ID and password for internet banking, the information contained in any accounts the Borrower may have with the Bank either singly or jointly with any other person and/or any other information which the Bank may receive in relation to any accounts the Borrower may have with the Bank either singly or jointly with any other person.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>42.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>The purpose in which the Bank collects the Personal Data (“Purpose”) include the following:-</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    ptext1 = "<font size=11>(a)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>to process the Borrower’s applications for any banking products and services;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>(b)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>to enable the Bank to consider whether to provide or continue to provide to the Borrower, any banking products and services;</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>(c)</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=11>to provide the Borrower with banking services;</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11>(d)</font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=11>for data processing or reporting purposes;</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9 = "<font size=11>(e)</font>"
    ptext_9 = (Paragraph(ptext9, styles['t1']))
    ptext10 = "<font size=11>to respond to any inquiries or complaints from the Borrower;</font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    ptext11 = "<font size=11>(f)</font>"
    ptext_11 = (Paragraph(ptext11, styles['t1']))
    ptext12 = "<font size=11>to promote, improve and further the provision of other services by the Bank or any member of the Group to the Borrower;</font>"
    ptext_12 = (Paragraph(ptext12, styles['Justify']))
    ptext13 = "<font size=11>(g)</font>"
    ptext_13 = (Paragraph(ptext13, styles['t1']))
    ptext14 = "<font size=11>for debt collection purposes;</font>"
    ptext_14 = (Paragraph(ptext14, styles['Justify']))
    ptext15 = "<font size=11>(h)</font>"
    ptext_15 = (Paragraph(ptext15, styles['t1']))
    ptext16 = "<font size=11>for enforcement of the Bank’s rights and obligations under the Security Documents;</font>"
    ptext_16 = (Paragraph(ptext16, styles['Justify']))
    ptext17 = "<font size=11>(i)</font>"
    ptext_17 = (Paragraph(ptext17, styles['t1']))
    ptext18 = "<font size=11>to comply with any legal and/or regulatory requirements;</font>"
    ptext_18 = (Paragraph(ptext18, styles['Justify']))
    ptext19 = "<font size=11>(j)</font>"
    ptext_19 = (Paragraph(ptext19, styles['t1']))
    ptext20 = "<font size=11>for processing the Borrower’s instructions and generating any correspondences, confirmation, advices and/or Statement of Account;</font>"
    ptext_20 = (Paragraph(ptext20, styles['Justify']))
    ptext21 = "<font size=11>(k)</font>"
    ptext_21 = (Paragraph(ptext21, styles['t1']))
    ptext22 = "<font size=11>to ensure that the information in the Bank’s “Customer Due Diligence” records are accurate; or</font>"
    ptext_22 = (Paragraph(ptext22, styles['Justify']))
    ptext23 = "<font size=11>(l)</font>"
    ptext_23 = (Paragraph(ptext23, styles['t1']))
    ptext24 = "<font size=11>for any direct marketing of the Bank’s banking and/or insurance products and services.</font>"
    ptext_24 = (Paragraph(ptext24, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4], ['', ptext_5, ptext_6],
            ['', ptext_7, ptext_8], ['', ptext_9, ptext_10], ['', ptext_11, ptext_12],
            ['', ptext_13, ptext_14], ['', ptext_15, ptext_16], ['', ptext_17, ptext_18],
            ['', ptext_19, ptext_20], ['', ptext_21, ptext_22], ['', ptext_23, ptext_24]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>42.4</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower’s Personal Data was collected from the information the Borrower has provided the Bank in the application form and any other document provided in relation to the Purpose.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>42.5</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>It is obligatory that the Borrower provides the Bank with the Personal Data the Bank requests from the Borrower. If the Borrower fails to provide the Bank with the Borrower’s Personal Data, the Bank may not be able to process and/or disclose the Borrower’s Personal Data in relation to the Purpose.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>42.6</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>The Borrower agrees and consents that the Bank may transfer the Personal Data outside of Malaysia. Other countries may not provide the same level of protection for data as compared to Malaysia. All Personal Data held by the Bank and the Group will be accorded a reasonable level of protection against any loss, misuse, modification, unauthorised or accidental access or disclosure, alteration or deletion.<br/><br/><br/><br/><br/><br/><br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11>42.7</font>"
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    ptext8 = "<font size=11>The Borrower is entitled to request in writing:-</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able = [[ptext_1, ptext_2], [ptext_3, ptext_4], [ptext_5, ptext_6],[ptext_7,ptext_8]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1 = "<font size=11>(a)</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2 = "<font size=11>for any information in relation to the Borrower’s Personal Data that the Bank holds or stores, upon payment of a prescribed fee;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>(b)</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4 = "<font size=11>for any information held or stored by the Bank to be updated, amended and/or corrected;</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>(c)</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6 = "<font size=11>for the Bank to limit the processing of the Borrower’s Personal Data held or stored by the Bank; and</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11>(d)</font>"
    ptext_7 = (Paragraph(ptext7, styles['t1']))
    ptext8 = "<font size=11>to make an enquiry or complaint in respect of the Bank’s processing of the Borrower’s Personal Data.</font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    able = [['', ptext_1, ptext_2], ['', ptext_3, ptext_4], ['', ptext_5, ptext_6],['', ptext_7, ptext_8]]
    t = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext2 = "<font size=11>The Borrower may direct the Borrower’s request to the servicing branch at which the Banking Facilities will be serviced, as stated in the Letter of Offer.<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>The Bank may charge a fee for processing the Borrower’s request for access or correction. The Bank may also refuse to comply with the Borrower’s request in respect of (a) or (b) above if the information supplied by the Borrower is insufficient (as determined by the Bank) or where such request may breach or violate any law or regulation or any other reason which the Bank deems not to be in its interest to do so. If the Bank refuses to comply with such request, the Bank will inform the Borrower of the Bank’s refusal and reason for its refusal.<br/><br/></font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext5 = "<font size=11>42.8</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>The Borrower is responsible for ensuring that the information the Borrower provides the Bank is accurate, complete and not misleading and that such information is kept up to date. <br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    ptext7 = "<font size=11>42.9</font>"
    ptext_7 = (Paragraph(ptext7, styles['Justify']))
    ptext8 = "<font size=11>If the Borrower subsequently withdraws the Borrower’s consent to process the Borrower’s Personal Data (other than for direct marketing purposes), the Bank will not be able to process and/or disclose the Borrower’s Personal Data in relation to the Purpose.<br/><br/></font>"
    ptext_8 = (Paragraph(ptext8, styles['Justify']))
    ptext9 = "<font size=11>42.10</font>"
    ptext_9 = (Paragraph(ptext9, styles['Justify']))
    ptext10 = "<font size=11>The Borrower may choose not to receive any direct marketing materials about the Bank’s services and products. The Borrower must write to the servicing branch at which the Banking Facilities will be serviced, as stated in the Letter of Offer or such other address notified by the Bank with the Borrower’s request and the Bank will delete the Borrower’s name from the Bank’s direct marketing mailing lists.<br/><br/></font>"
    ptext_10 = (Paragraph(ptext10, styles['Justify']))
    able = [['', ptext_2], ['', ptext_3], [ptext_5, ptext_6], [ptext_7, ptext_8],[ptext_9,ptext_10]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 43</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>SEVERABILITY</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>43.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>If any of the provisions of this Agreement is or becomes invalid or unenforceable, the invalid or unenforceable provision is to be treated as not having been included in this Agreement; the remainder of this Agreement is to continue to be effective and in force and is not to be affected in any way by the invalid or unenforceable provision.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = '<font size=12><b>SECTION 44</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>NON-WAIVER</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>44.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower agrees that if the Borrower breaches any of the terms and conditions governing the Housing Loan or the Property, the Bank may at its sole discretion decide not to exercise any right which the Bank may have in relation to the Borrower’s breach.<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>44.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>Any decision of the Bank not to exercise any right which the Bank may have in relation to the Borrower’s breach is not to be treated as a waiver of the Bank’s rights and the Bank retains the right at any time afterwards to strictly enforce or to insist on the Bank’s rights in relation to that breach or any subsequent breach by the Borrower.</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 45</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>NON-ACQUIESENCE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>45.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower agrees that, even if the Bank may not have exercised any remedy available to the Bank immediately upon default by the Borrower or even if the Bank may have accepted moneys from the Borrower or any security party after such default, the Bank shall not be held to have acquiesced to such default and the Bank may at any time after that exercise all or any of the remedies available to the Bank under this Agreement, the Security Documents and any applicable law. Any delay on the part of the Bank in taking steps to enforce the remedies available to it under this Agreement, the Security Documents or any applicable law shall not in any way affect the Bank’s right to take those steps.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 46</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>CUMULATIVE REMEDIES</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>46.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The rights, remedies, powers, and privileges provided under this Agreement are cumulative and are not exclusive of any rights, remedies, and privileges provided by law, in any other agreement between the parties or otherwise.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 47</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>INCONSISTENCIES</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>47.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The provisions of this Agreement are additional to and do not in any way deviate from the terms and conditions contained in the Letter of Offer; if there is any inconsistency between any of the provisions of this Agreement and the terms and conditions contained in the Letter of Offer, the terms and conditions contained in the Letter of Offer will prevail, that is, the terms and conditions contained in the Letter of Offer will take precedence.<br/><br/></font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3 = "<font size=11>47.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['Justify']))
    ptext4 = "<font size=11>Although the Schedules to this Agreement form part of this Agreement, if any of the provisions in any of the Schedules to this Agreement is inconsistent with the provisions contained in the main text of this Agreement, the provision in the Schedule will prevail, that is, the provision in the relevant Schedule will take precedence.<br/><br/></font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5 = "<font size=11>47.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['Justify']))
    ptext6 = "<font size=11>In the event of any conflict or discrepancy between the Security Document and this Agreement, provisions of the Security Document will prevail for the purpose of interpretation and enforcement of the Security Document.<br/><br/></font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able = [[ptext_1, ptext_2],[ptext_3,ptext_4],[ptext_5,ptext_6]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 48</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>GOVERNING LAW</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>48.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>This Agreement and the Security Documents are to be governed by and interpreted in accordance with the laws of Malaysia and the Borrower agrees that, upon the Borrower’s acceptance of the Housing Loan, the Borrower is deemed to have unconditionally and irrevocably:-</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1,11))
    ptext1  = "<font size=11>48.1.1</font>"
    ptext_1 = (Paragraph(ptext1, styles['t1']))
    ptext2  = "<font size=11>agreed that any dispute involving this Agreement and the Security Documents may be submitted to the courts of law within and outside of Malaysia;</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    ptext3  = "<font size=11>48.1.2</font>"
    ptext_3 = (Paragraph(ptext3, styles['t1']))
    ptext4  = "<font size=11>agreed not to raise any objection to any dispute being submitted in any particular court of law on the basis that it is not the correct or most convenient court for the dispute to be submitted to; and</font>"
    ptext_4 = (Paragraph(ptext4, styles['Justify']))
    ptext5  = "<font size=11>48.1.3</font>"
    ptext_5 = (Paragraph(ptext5, styles['t1']))
    ptext6  = "<font size=11>consented to the service on the Borrower of any demand by the Bank and of any court documents by registered mail or by any other manner allowed by the relevant laws.</font>"
    ptext_6 = (Paragraph(ptext6, styles['Justify']))
    able    = [['',ptext_1,ptext_2],['',ptext_3,ptext_4],['',ptext_5,ptext_6]]
    t       = Table(able, (1 * cm, 2.5 * cm, 11.7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=12><b>SECTION 49</b></font>'
    ptext1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = '<font size=12><b>LEGAL ADVICE</b></font>'
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext1, ptext_2]]
    t = Table(able, (3 * cm, 13 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>49.1</font>"
    ptext_1 = (Paragraph(ptext, styles['Justify']))
    ptext2 = "<font size=11>The Borrower confirms that the Borrower has been advised to seek independent legal advice before accepting the Housing Loan and before signing the Letter of Offer and the Security Documents prepared by the Bank or the Bank’s solicitors.</font>"
    ptext_2 = (Paragraph(ptext2, styles['Justify']))
    able = [[ptext_1, ptext_2]]
    t = Table(able, (2 * cm, 14 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    end   = "<font size=11>-End of Page-</font>"
    end_1 = (Paragraph(end,styles['Title']))
    Story.append(end_1)
    Story.append(PageBreak())
    partc = "<font size=11>PART C</font>"
    part_c = (Paragraph(partc, styles['Title']))
    Story.append(part_c)
    temporary = "<font size=11>(Offer Letter for loan will be here)</font>"
    temporary1 = (Paragraph(temporary, styles['Normal']))
    Story.append(temporary1)
    Story.append(PageBreak())
    exe = "<font size=11><u>EXECUTION</u></font>"
    exe1= (Paragraph(exe,styles['Normal']))
    Story.append(exe1)
    Story.append(Spacer(1,11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    for i in range(len(borrower)):
        ptext1 = "<font size=11> Signed by the borrower</font>"
        ptext_1 = Paragraph(ptext1, styles['Normal'])
        ptext2 = "<font size=11>in the presence of : </font>"
        ptext_2 = Paragraph(ptext2, styles['Justify'])
        ptext3 = "<font size=11>Name: <b>%s</b></font>"
        ptext3 = ptext3 % borrower
        ptext_3 = Paragraph(ptext3, styles['Justify'])
        ptext4 = "<font size=11>NRIC No: <b>%s</b></font>"
        ptext4 = ptext4 % NRIC
        ptext_4 = Paragraph(ptext4, styles['Justify'])
        able = [[ptext_1,")",""],
                [ptext_2, ")", "....................................................."],
                [" ", " ", ptext_3],
                [" ", " ", ptext_4]]
        t = Table(able, (6 * cm, 2 * cm, 8 * cm))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            #('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            #('BOX', (0, 0), (-1, -1), 1.50, colors.white),
        ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    name   = "<font size=12><b>BANK</b></font>"
    name_1 = Paragraph(name,styles['Justify'])
    Story.append(name_1)
    ptext1 = "<font size=11> Signed for and behalf</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext2 = "<font size=11><b>%s</b></font>"% bank
    ptext_2 = Paragraph(ptext2,styles['Justify'])
    ptext3 = "<font size=11>by its duly authorised representative</font>"
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext4 = "<font size=11>in the presence of:</font>"
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    able = [[ptext_1,')',''],[ptext_2,')',""],[ptext_3,')',''],[ptext_4,')','']]
    t = Table(able, (6 * cm, 2 * cm, 8 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))

    Story.append(t)
    Story.append(PageBreak())
    sched = "<font size=11><b>SCHEDULE</b></font>"
    sched_1 = Paragraph(sched, styles['Title'])
    Story.append(sched_1)
    word = "<font size =11>(To be read and construed as an essential part of this Agreement)</font>"
    word_1 = Paragraph(word, styles['Title'])
    Story.append(word_1)
    ptext = "<font size=11><b>Section</b></font>"
    ptext_ = Paragraph(ptext, styles['Justify'])
    ptext1 = "<font size=11><b>Item</b></font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext2 = "<font size=11><b>Particulars/Details</b></font>"
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext3 = "<font size=11><br/>1<br/><br/></font>"
    ptext_3 = Paragraph(ptext3,styles['Justify'])
    ptext4 = "<font size=11><br/>Date of this Agreement<br/><br/></font>"
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    ptext5 = "<font size=11><br/>%s<br/><br/></font>"%datetime
    ptext_5 = Paragraph(ptext5,styles['Justify'])
    ptext6 = "<font size=11><br/>2<br/><br/></font>"
    ptext_6 = Paragraph(ptext6, styles['Justify'])
    ptext7 = "<font size=11><br/>The Bank’s Address<br/><br/></font>"
    ptext_7 = Paragraph(ptext7, styles['Justify'])
    ptext8 = "<font size=11>%s</font>" %bank_address
    ptext_8 = Paragraph(ptext8, styles['Justify'])
    ptext9 = "<font size=11><br/>3<br/><br/></font>"
    ptext_9 = Paragraph(ptext9, styles['Justify'])
    ptext10 = "<font size=11><br/>Name, particulars and address of the Borrower<br/><br/></font>"
    ptext_10 = Paragraph(ptext10, styles['Justify'])
    ptext11 = "<font size=11><br/><b>%s<br/>%s<br/>%s</b><br/><br/></font>"%(borrower,borrower_address,NRIC)
    ptext_11 = Paragraph(ptext11,styles['Justify'])
    ptext12 = "<font size=11><br/>4<br/><br/></font>"
    ptext_12 = Paragraph(ptext12, styles['Justify'])
    ptext13 = "<font size=11><br/>Principal amount of Housing Loan<br/><br/></font>"
    ptext_13 = Paragraph(ptext13, styles['Justify'])
    the_price = "RM{:,.2f}".format(int(loan_ammount))
    ptext14 = "<font size=11><br/>*Ringgit Malaysia<br/><br/>(%s)<br/><br/><br/><br/>#Ringgit Malaysia<br/><br/><br/><br/><br/>(%s  such sums as evidenced by the ad valorem stamp duty paid and endorsed from time to time on this Agreement.</font>" %(the_price,the_price)
    ptext_14 = Paragraph(ptext14, styles['Justify'])
    ptext15 = "<font size=11><br/>5<br/><br/></font>"
    ptext_15 = Paragraph(ptext15, styles['Justify'])
    ptext16 = "<font size=11><br/>Margin<br/><br/></font>"
    ptext_16 = Paragraph(ptext16, styles['Justify'])
    ptext17 = "<font size=11> <br/>%s  per annum<br/><br/><br/><br/><br/><br/><br/>or such other rate that the Bank may prescribe at any time.</font>" %loan_margin
    ptext_17 = Paragraph(ptext17,styles['Justify'])
    ptext18 = "<font size=11>6</font>"
    ptext_18 = Paragraph(ptext18,styles['Justify'])
    ptext19 = "<font size=11>Property</font>"
    ptext_19 = Paragraph(ptext19,styles['Justify'])
    ptext20 = "<font size=11><br/><br/><br/><br/><br/><br/><br/><br/><br/></font>"
    ptext_20 = Paragraph(ptext20, styles['Justify'])
    able= [[ptext_,ptext_1,ptext_2],[ptext_3,ptext_4,ptext_5],[ptext_6,ptext_7,ptext_8],[ptext_9,ptext_10,ptext_11],[ptext_12,ptext_13,ptext_14],[ptext_15,ptext_16,ptext_17],[ptext_18,ptext_19,ptext_20]]
    t = Table(able, (2.5 * cm, 5 * cm, 7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    doc.multiBuild(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
