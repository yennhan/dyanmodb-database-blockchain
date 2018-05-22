# coding=utf-8
#Leow Yenn Han
#leowyennhan@gmail.com
import time
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table,TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.lib.units import inch
from reportlab.lib.units import cm,mm
from reportlab.lib import colors
from num2words import num2words


class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    # ----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    # ----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    # ----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(195 * mm, 272 * mm, page)


# ----------------------------------------------------------------------


def pdf_generator(snp_id,datetime,owner,NRIC,newOwner,agreed_price,owner_address,new_owner_address,interest_rate,RPGT,company,property_description,house_title,sold_house_address,master_title,charge_or_assign):

    doc = SimpleDocTemplate(snp_id+".pdf",rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    Story=[]
    logo = "static/img/logo.svg"
    im   =  Image(logo, 2*inch, 2*inch)

    ptext = '<font size=11><b>AN AGREEMENT</b> made on %s</font>' %datetime
    Story.append(Paragraph(ptext,styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11>BETWEEN</font>'

    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))

    ptext = '<font size=11>The individual(s)/entity(ies) whose particulars are set out in <b> Item B of Schedule 1 </b>hereto (hereinafter individually/collectively referred to as "<b>the Vendor</b>" of the one part;</font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11>AND</font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = '<font size=11><b>%s </b> with its registered address at %s (hereinafter referred to as "<b>the Purchaser</b>" of the other part</font> '
    ptext =  ptext %(newOwner,new_owner_address)
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext ='<font size=11><b>WHEREAS</b></font>'
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))

    ptext1  = "<font size=11>It is the Vendor's presentation that he/she/it is the legal and beneficial owner of the property described in <b>Item C of Schedule 1 </b> hereto (hereinafter referred to as ""<b>the said Property</b>"").""</font>"
    ptext2  = "<font size=11>It is the Vendor’s representation that the said Property is free from any encumbrances save and except as described in Item D of Schedule 1 (if applicable).</font>"
    ptext3  = "<font size=11>The Vendor has agreed to sell and the Purchaser has agreed to purchase the said Property with vacant possession on an “as is where is basis” and free from all encumbrances and upon the terms and conditions hereinafter appearing.</font>"
    ptext4  = "<font size=11>The Vendor elects not to be represented by any solicitors and the Purchaser is represented by Messrs L P Gee & Co. in this sale and purchase transaction.</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    able    = [['1. ',ptext_1],['2. ',ptext_2],['3. ',ptext_3],['4. ',ptext_4]]
    t       = Table(able,(1*cm,15*cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><b>NOW THIS AGREEMENT WITNESSETH </b> as follows:- </font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>AGREEMENT TO SELL AND PURCHASE</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>In consideration of the terms and considerations of this Agreement and Purchase Price as set out in <b>Item 2A of Schedule 2 herein</b> (hereinafter referred to as “<b>the Purchase Pric</b>”), the Vendor hereby agrees to sell and the Purchaser hereby agrees to purchase the said Property free from all encumbrances and with vacant possession on an “as is where is basis” together with Fixtures and Fittings. </font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = "<font size=11><seq>.  <b>AGREEMENT TO SELL AND PURCHASE</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11> The Purchaser shall pay the Purchase Price [where applicable, less any Redemption Sum payable to the Vendor’s Chargee/Assignee, outstanding Quit Rent and/or Assessments, outstanding maintenance charges, outstanding utilities and any other deductions as may be agreed between the Vendor and Purchaser (collectively referred to as “<b>Deductions</b>”)] to the Vendor on or before the date stipulated in <b>Item 2B of Schedule 2</b> hereto (hereinafter referred to as “<b>Completion Date</b>”) <b>PROVIDED THAT</b>:</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    able    = [['(a) ', ptext_1]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>the Vendor has deposited with the Purchaser’s Solicitors all necessary valid instruments and documents to complete the sale and purchase transaction herein including but not limited to the original individual title for the Property and Memorandum of Transfer (if applicable); original application form for authority’s consent for transfer (if applicable); original previous Sale and Purchase Agreement(s) and Deed(s) of Assignment together with original ‘Sijil Setem’ and ‘Notis Taksiran’ (if applicable); certified true copy of Vendor’s identity card / Company Forms 24, 44 and 49, Memorandum of Articles & Association and Shareholders’ Resolution for the sale; current Quit Rent and Assessment Receipts and all other documents required by the Purchaser;</font>"
    ptext2  = "<font size=11>Where applicable, all necessary instruments and documents from the Vendor’s Chargee/Assignee including but not limited to Redemption Statement, duly executed and stamped Discharge of Charge / duly executed and stamped Deed of Receipt and Reassignment, duly revoked Power of Attorney and all other related documents;</font>"
    ptext3  = "<font size=11>Legal / Vacant possession of the Property is delivered to the Purchaser simultaneously with the payment of the Purchase Price (less Deductions). </font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    able    = [[' ','i)', ptext_1],[' ','ii)', ptext_2],[' ','iii)', ptext_3]]
    t       = Table(able, (2 * cm, 0.5 * cm,15*cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (2, 2), 0.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>. <b>MEMORANDUM OF TRANSFER / DEED OF ASSIGNMENT</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11> The parties hereby undertake to perform and comply with the requirements to be fulfilled by them on their part for the execution of the Memorandum of Transfer [“<b>MOT</b>”] / Deed of Assignment by way of Transfer [“<b>DOA</b>”] where applicable, in favour of the Purchaser. Upon the execution of the MOT / DOA, the MOT / DOA shall be held by the Purchaser’s Solicitors who are irrevocably authorized to submit the MOT / DOA for adjudication at the appropriate time subject to the instructions of the Purchaser.</font>"
    ptext2  = "<font size=11>Upon the MOT / DOA being adjudicated, the Purchaser shall pay the stamp duty thereon upon being informed by the Purchaser’s Solicitors.</font>"
    ptext3  = "<font size=11>For the avoidance of doubt, notwithstanding the reference of “Completion Date” in this Agreement, this sale and purchase transaction is not and shall not be deemed complete unless and until the Memorandum of Transfer is registered in favour of the Purchaser.   </font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    able    = [['(a) ', ptext_1],['(b) ',ptext_2],['(c) ',ptext_3]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>DELIVERY OF DOCUMENTS</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>Notwithstanding anything to the contrary in the event that the Vendor fails to deliver the documents in Clause 2(a) and any other documents required by the Purchaser, the obligation of the Purchaser to pay the Purchase Price (less Deductions) shall be automatically suspended and the Completion Date shall accordingly be extended by such number of days of delay by the Vendor in performing the above covenants without any interest being payable by the Purchaser whatsoever but without prejudice to the other rights of the Purchaser against the Vendor at law and/or in equity. </font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = "<font size=11><seq>.  <b>DEFAULT BY PURCHASER</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>It is hereby agreed between the parties hereto that if the Purchaser fail to pay the Purchase Price and the Vendor are willing, able and ready to complete the sale of the said Property in accordance with the terms of this Agreement, the Vendor shall the right to terminate this Agreement by giving 14 days written notice to the Purchaser. Upon the termination of the Agreement by the Vendor, the Purchaser shall return to the Vendor all documents furnished by the Vendor including original individual document of title and all instruments executed for the purposes of this Agreement shall be null and void. Thereafter, neither party hereto shall have any claims against the other, and the Vendor shall be at liberty to re-sell the said Property in such manner as the Vendor shall think fit. </font>"
    Story.append(Paragraph(ptext,styles['Justify']))
    Story.append(Spacer(1,11))
    ptext = "<font size=11><seq>.  <b>DEFAULT BY VENDOR</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>It is also further agreed between the parties hereto that if the Purchaser have or is able, ready and willing to pay the Purchase Price (less Deductions) and the Vendor fails and/or is unable and/or refuse to complete the sale in accordance with the terms of this Agreement, the Purchaser shall be entitled to either:-</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>specific performance and/or other legal remedies available to them; OR </font>"
    ptext2  = "<font size=11>terminate this Agreement and demand the return of all monies so paid by the Purchaser to the Vendor or on account of the Vendor pursuant to this Agreement and the Vendor hereby further agrees and shall in addition pay to the Purchaser a further sum of Ringgit Malaysia Twenty Thousand (RM20,000-00) only absolutely as agreed liquidated damages failing which the Vendor shall pay interest at the rate of %s per annum calculated on a daily basis on any part of the sums remaining unrefunded and unpaid to the Purchaser from the date of demand until the full refund is made to the Purchaser. After such refund and payment, this Agreement shall become null and void with each party having no claim whatsoever against the other.</font>"
    ptext2  = ptext2 %interest_rate
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    able    = [['(a) ', ptext_1],['(b) ',ptext_2]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>PASSING OF INTEREST IN THE PROPERTY</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The Vendor hereby expressly agrees and confirms that as from the date of the Purchaser depositing the Purchase Price (less Deductions) with the Vendor, he shall have no right, title, interest or anything whatsoever in and to the said Property and the Vendor hereby expressly further acknowledges that as from the date thereof the Purchaser is the person entitled to the legal and equitable title and interest in and to the said Property.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>DELIVERY OF VACANT POSSESSION</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The Vendor shall deliver vacant possession of the said Property on an “as is where is basis” to the Purchaser in the state and condition as at the date of this Agreement, simultaneously with the payment of the Purchase Price (less Deductions) to the Vendor.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>NON-REGISTRATION OF DOCUMENTS</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>Without prejudice to Clause 6, if after completion of this Agreement, the Memorandum of Transfer of the said Property cannot be registered in favour of the Purchaser free from all encumbrances by any reason whatsoever including but not limited to any caveat, prohibitory orders or other encumbrances save for any caveats prohibitory orders or encumbrances lodged or entered by Purchaser or any one lawfully claiming through the Purchaser, it shall be the duty of the Vendor to remove or cause to be removed forthwith at the Vendor’s own cost and expense such reason of obstruction including but not limited to caveat, prohibitory orders, or other encumbrances in order to enable the Purchaser to be registered as proprietor free from all encumbrances. </font>"
    ptext2  = "<font size=11>In the alternative, the Purchaser shall be entitled at their option to request the Vendor to refund all monies paid to the Vendor or in favour of the Vendor pursuant to this Agreement free of interest within Seven (7) days of demand whereupon the Vendor shall make such refund within the said Seven (7) days failing which the Vendor shall pay interest at the rate of %s per annum calculated on a daily basis on all monies remaining unrefunded to the Purchaser from the expiry of the said Seven (7) working days until the full refund is made to the Purchaser and thereafter this Agreement shall be treated as terminated.</font>"
    ptext2  = ptext2 % interest_rate
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    able    = [['(a) ', ptext_1], ['(b) ', ptext_2]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>REAL PROPERTY GAINS TAX</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>Each party shall respectively notify the Director-General of Inland Revenue, Malaysia (hereinafter referred as “the Director General”) of the acquisition and disposal of the said Property within sixty (60) days from the date of this Agreement. </font>"
    ptext2  = "<font size=11>If applicable, the Purchaser agrees to pay on behalf of the Sum amounting to %s of the Purchase Price to be paid to the Director General of Inland Revenue in accordance with the provisions of the Real Property Gains Tax Act, 1976, and the difference between the total tax imposed by the Director General and the said Sum upon receipt of the notice of assessment from the Director General within the period prescribed therein. </font>"
    ptext3  = "<font size=11>Upon the issuance by the Director-General of a Certificate of Clearance or a Certificate of Non-Chargeability or payment of the Real Property Gains Tax, as the case maybe, any excess payment derived from the said Sum after the deduction of any real property gains tax imposed by the Director General shall be refunded to the Purchaser.</font>"
    ptext2  = ptext2 % RPGT
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    able    = [['(a) ', ptext_1], ['(b) ', ptext_2],['(c) ',ptext_3]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b>GOVERNMENT ACQUISITION</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>The Vendor hereby covenant with the Purchaser that he/she/it has not received any notice from the Government or any proper authorities having power in that behalf to acquire the said Property or any part or parts thereof.</font>"
    ptext2  = "<font size=11>It is hereby agreed between the parties hereto that in the event of the Government or any proper Authorities having power on that behalf acquiring the said Property or any part or parts thereof for any purpose whatsoever after the date of this Agreement and before the Purchase Price has been paid to the Vendor, the Vendor shall immediately by writing notify the Purchaser upon receiving notice of such intended acquisition or declaration and the Purchaser shall forthwith be entitled by notice in writing to the Vendor, elect:-</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    able    = [['(a) ', ptext_1], ['(b) ', ptext_2]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1  = "<font size =11>to rescind this Agreement whereupon the Vendor shall within Fourteen (14) working days from the date of receipt of the Purchaser’ notice refund to the Purchaser free of interest all monies already paid by the Purchaser to the Vendor pursuant to this Agreement and the Purchaser failing which the Vendor shall pay interest at the rate of %s per annum calculated on a daily basis on all monies remaining unrefunded to the Purchaser from the expiry of the said Fourteen (14) working days until the full refund is made to the Purchaser and thereafter this Agreement shall be terminated and shall be null and void and of no effect or force and neither party hereto shall have any further right against the other save and except for any antecedent breach of this Agreement; or</font>"
    ptext2  = "<font size =11>require the Vendor to serve notice upon such authority within Fourteen (14) working days from the date of receipt of the Purchaser’ election of the Purchaser’ interest in the said Property under the terms and conditions of this Agreement and thereafter the Purchaser shall be absolutely entitled to the whole of the benefit of any arrangement made or the compensation (if any) awarded by such acquiring authority in respect of such acquisition and the Vendor shall do all acts and things and execute and sign all documents to enable the Purchaser to procure such arrangement or compensation Provided Always That the Purchaser shall have paid the Purchase Price (less Deductions) in accordance with the terms herein. </font>"
    ptext1  = ptext1 % interest_rate
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    able    = [[' ', '(i)', ptext_1], [' ', '(ii)', ptext_2]]
    t       = Table(able, (2 * cm, 0.5 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (2, 2), 0.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11><seq>.  <b> RISK AGAINST FIRE AND OTHER HAPPENINGS</b></font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The parties hereto agree that in the event that the said Property is destroyed by fire or other happenings beyond the control of the Vendor before vacant possession of the said Property is delivered to the Purchaser, the Purchaser shall have the option to treat this Agreement as terminated whereupon the Vendor shall refund to the Purchaser all the monies paid to the Vendor or on account of the Vendor pursuant to this Agreement without any interest thereon failing which the Vendor shall pay interest at the rate of %s per annum calculated on a daily basis on any part of the sums remaining unrefunded to the Purchaser from the date of demand until the full refund is made to the Purchaser whereupon this Agreement shall be terminated.</font>"
    ptext = ptext % interest_rate
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> APPORTIONMENT OF QUIT RENT, ASSESSMENT AND OTHER LAWFUL OUTGOINGS</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['13. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>The quit rent, assessment, and other lawful outgoings payable in respect of the said Property to the relevant authorities shall be apportioned between the Vendor and the Purchaser as at the date of delivery of vacant possession to the Purchaser. The Vendor shall also indemnify the Purchaser in respect of any penalty imposed in respect of any late payment by the Vendor in respect of such quit rent, assessment and other lawful out goings.</font>"
    ptext2  = "<font size=11>The Purchaser hereby agree to pay all the lawful outgoings payable to the relevant authorities in respect of the said Property from the date vacant possession of the said Property is delivered to the Purchaser.</font>"
    ptext3  = "<font size=11>Upon completion of the sale and purchase herein and the delivery of vacant possession of the said Property to the Purchaser, the Purchaser shall take all necessary steps to notify the relevant authorities of the change of ownership of the said Property so that all future bills in respect of quit rents, assessment rates, sewerage and utility charges and all other lawful whatsoever in respect of the said Property will be directed to the Purchaser. The Purchaser shall indemnify and keep the Vendor indemnified in respect of all losses, damages, fines and penalties arising from the Purchaser’s breach of this Clause and/or from late payment or non-payment of all quit rent, assessment, water, electricity and indah water charges payable in respect of the said Property from the date vacant possession of the said Property is delivered to the Purchaser.</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    able    = [['(a) ', ptext_1], ['(b) ', ptext_2], ['(c) ', ptext_3]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = "<font size=11><b>LODGEMENT OF PRIVATE CAVEAT</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['14. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11> At any time after the date hereof, the Purchaser shall be entitled at their own cost and expense to present and register a private caveat against the Property for the purpose of protecting the Purchaser’s interest in the Property and prohibiting any dealing by the Vendor in the Property prior to the completion or termination of this Agreement <b>PROVIDED FURTHER THAT</b> the Purchaser shall simultaneously execute a withdrawal of private caveat and deposit the same together with the requisite registration fees with the Purchaser’s Solicitors who are hereby authorized by the Purchaser to remove or cause to be removed the aforesaid private caveat upon lawful termination of this Agreement.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> COSTS AND EXPENSES</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['15. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The Purchaser shall bear the costs for this Sale and Purchase Agreement. The costs for attending to the Memorandum of Transfer together with the stamp duties and registration fees thereof, inclusive of penalty, if any, thereof shall be borne and paid by the Purchaser.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> KNOWLEDGE OR ACQUIESCENCE</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['16. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>Knowledge or acquiescence of either party hereto of or in any breach of any of the conditions or covenants herein contained shall not operate as or be deemed to be a waiver of such conditions or covenants or any of them and notwithstanding such knowledge or acquiescence each party hereto shall be entitled to exercise their respective rights under this Agreement and to require strict performance by the other of the terms and conditions herein. </font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> SEVERABILITY</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['17. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>If any one or more of the provisions contained in this Agreement shall be invalid or unenforceable in any respect the legality and enforceability of the remaining provisions contained herein shall not in any way be affected or impaired.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> HEADINGS</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['18. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The headings of each of the Clauses herein contained are inserted merely for convenience of reference and shall be ignored in the interpretation and construction of any of the provisions herein contained. </font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))

    ptext = "<font size=11>  <b> TIME OF THE ESSENCE</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['19. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>Time whenever mentioned shall be of the essence of this Agreement.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> SUCCESSORS BOUND</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['20. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>This Agreement shall be binding upon the successors-in-title legal representatives, administrators, nominees and permitted assigns of the parties hereto.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = "<font size=11>  <b> SERVICE OF NOTICE OR DEMAND</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['21. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>Any notice, request or demand requiring to be served by either party hereto to the other under the provisions of this Agreement shall be in writing and shall be deemed to be sufficiently served:-</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>if it is given by the party or his solicitors by post under registered cover addressed to the other party to be served at his or its address hereinbefore mentioned or to his solicitors and in such a case it shall be deemed (whether actually delivered or not) to have been served at the time of posting of the notice; or </font>"
    ptext2  = "<font size=11>if it is given by the party or his or solicitors and despatched by hand to the party to be served or his solicitors; or</font>"
    ptext3  = "<font size=11>if given by facsimile it shall be deemed served to the other party or his solicitors when the transmitting machine registers the confirmation that the transmission has been successfully made showing the recipient’s facsimile number on the sender’s receipt of a confirmed log print-out for the transmission regarding the date time and transmission of all pages and shall be addressed to the parties or their solicitors or such address as any of the parties may designate from time to time.</font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    able    = [['(i) ', ptext_1], ['(ii) ', ptext_2], ['(iii) ', ptext_3]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> NOTIFICATION OF CHANGE OF OWNERSHIP OF THE SAID PROPERTY</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['22. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>The Purchaser and the Vendor shall where necessary inform all relevant authorities of the change of ownership of the said Property after completion of the sale and purchase herein at their cost and expense. It is hereby agreed that it shall not be the responsibility of the Purchaser’s Solicitors to perform any of the foregoing matters.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext = "<font size=11>  <b> INTERPRETATION</b></font>"
    ptext = Paragraph(ptext, styles['Justify'])
    able  = [['23. ', ptext]]
    t     = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext   = "<font size=11>In this Agreement unless there is something in the subject or context inconsistent with such construction or unless it is otherwise expressly provided:-</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    ptext1  = "<font size=11>the expression “the Vendor” and “the Purchaser” shall include their respective successors personal representatives and assigns of the Vendor and the Purchaser and where two or more persons are included in any of the aforesaid expression this Agreement binds such persons jointly and severally;</font>"
    ptext2  = "<font size=11>words importing the masculine gender only include the feminine and neuter genders;</font>"
    ptext3  = "<font size=11>words importing the singular number only include the plural and vice versa;</font>"
    ptext4  = "<font size=11>words applicable to human beings include any body of persons corporate or unincorporate; </font>"
    ptext5  = "<font size=11>the phrase “working day” shall exclude Saturdays, Sundays, public holidays and state holidays in Selangor and/or Kuala Lumpur; and </font>"
    ptext6  = "<font size=11>	the word “month” shall mean the period of time which ends on the same date as it commenced in the previous month but if there is no numerically corresponding date in the following month, then the period shall end on the last day of the month PROVIDED ALWAYS that if the Completion Date falls on a non-working day, then the period shall end on the next working day. </font>"
    ptext_1 = Paragraph(ptext1, styles['Justify'])
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    ptext_5 = Paragraph(ptext5, styles['Justify'])
    ptext_6 = Paragraph(ptext6, styles['Justify'])
    able    = [['(a) ', ptext_1],['(b) ', ptext_2],['(c) ', ptext_3],['(d) ', ptext_4],['(e) ', ptext_5],['(f) ', ptext_6]]
    t       = Table(able, (1 * cm, 15 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext   = "<font size=11> (The rest of this page has been intentionally left blank)</font>"
    ptext_1 = Paragraph(ptext, styles['Justify'])
    able    = [[' ', ptext_1, ' ']]
    t       = Table(able, (5 * cm, 15 * cm, 1 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (2, 2), 0.50, colors.white, None, (2, 2, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.50, colors.white),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = "<font size=11><b>IN WITNESS WHEREOF</b> the parties hereto have hereunto set their respective hands/seal the day and year first abovewritten.</font>"
    Story.append(Paragraph(ptext, styles['Justify']))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))

    ptext   = "<font size=11>   Signed by</font>"
    ptext   = Paragraph(ptext, styles['Justify'])
    ptext1  = "<font size=11>the above mentioned Purchaser</font>"
    ptext_1 = Paragraph(ptext1,styles['Normal'])
    ptext2  = "<font size=11>in the presence of : </font>"
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext3  = "<font size=11>Name: <b>%s</b></font>"
    ptext3  = ptext3 % owner
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext4  = "<font size=11>NRIC No: <b>%s</b></font>"
    ptext4  = ptext4 % NRIC
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    able    = [[ptext, ")"," "],[" ",")"," "],[ptext_1,")"," "],[ptext_2,")","....................................................."],[" "," ",ptext_3],[" "," ",ptext_4]]
    t       = Table(able, (6 * cm, 2 * cm,7 * cm))
    t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
        ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    if company!="":
        ptext   = "<font size=11>   The Common Seal of the</font>"
        ptext   = Paragraph(ptext, styles['Justify'])
        ptext1  = "<font size=11>abovenamed Vendor (a Company)</font>"
        ptext_1 = Paragraph(ptext1, styles['Normal'])
        ptext2  = "<font size=11>is hereunto affixed </font>"
        ptext_2 = Paragraph(ptext2, styles['Justify'])
        ptext3  = "<font size=11>in the presence of :-</font>"
        ptext_3 = Paragraph(ptext3, styles['Justify'])
        able    = [[ptext, ")", " "], [ptext_1, ")", " "], [ptext_2, ")", " "],[ptext_3, ")", ""]]
        t       = Table(able, (6 * cm, 2 * cm, 7 * cm))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
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
        ptext   = "<font size=11>   Signed by</font>"
        ptext   = Paragraph(ptext, styles['Justify'])
        ptext1  = "<font size=11><b>%s</b></font>"
        ptext1  = ptext1 % company
        ptext_1 = Paragraph(ptext1, styles['Normal'])
        ptext2  = "<font size=11>the above mentioned Purchaser </font>"
        ptext_2 = Paragraph(ptext2, styles['Justify'])
        ptext3  = "<font size=11>in the presence of :-</font>"
        ptext_3 = Paragraph(ptext3, styles['Justify'])
        able    = [[ptext, ")", " "], [ptext_1, ")", " "], [ptext_2, ")", " "],['',')',''],[ptext_3, ")", ""]]
        t       = Table(able, (6 * cm, 2 * cm, 7 * cm))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
        ]))
        Story.append(t)

    ptext = "<font size=11>   Signed by</font>"
    ptext = Paragraph(ptext, styles['Justify'])
    ptext1 = "<font size=11>the above mentioned Vendor</font>"
    ptext_1 = Paragraph(ptext1, styles['Normal'])
    ptext2 = "<font size=11>in the presence of : </font>"
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext3 = "<font size=11>Name: <b>%s</b></font>"
    ptext3 = ptext3 % newOwner
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext4 = "<font size=11>NRIC No: <b>%s</b></font>"
    ptext4 = ptext4 % NRIC
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    able = [[ptext, ")", " "], [" ", ")", " "], [ptext_1, ")", " "],
                [ptext_2, ")", "....................................................."], [" ", " ", ptext_3],
                [" ", " ", ptext_4]]
    t = Table(able, (6 * cm, 2 * cm, 7 * cm))
    t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1.50, colors.white, None, (2, 2, 1)),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1.50, colors.white),
        ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    Story.append(PageBreak())
    ptext = "<font size=11><u>Schedule 1</u></font>"
    Story.append(Paragraph(ptext, styles['title']))
    Story.append(Spacer(1, 11))

    ptext    = "<font size=11><b>Item</b></font>"
    ptext    = Paragraph(ptext, styles['Justify'])
    ptext11  = "<font size=11><b>Particulars</b></font>"
    ptext_11 = Paragraph(ptext11, styles['Justify'])
    ptext1   = "<font size=11><b>1A</b></font>"
    ptext_1  = Paragraph(ptext1, styles['Justify'])
    ptext2   = "<font size=11><b>1B</b></font>"
    ptext_2  = Paragraph(ptext2, styles['Justify'])
    ptext3   = "<font size=11><b>1C</b></font>"
    ptext_3  = Paragraph(ptext3, styles['Justify'])
    ptext4   = "<font size=11><b>1D</b></font>"
    ptext_4  = Paragraph(ptext4, styles['Justify'])
    ptext5   = "<font size=11>The Property is Charged or Assigned to</font>"
    ptext_5  = Paragraph(ptext5,styles['Justify'])
    ptext6   = "<font size=11>Chargee/Assignee: </font>"
    if charge_or_assign !='':
        ptext6 = ptext6 + '%s'
        ptext6 = ptext6 % charge_or_assign
    else:
        ptext6 = ptext6 + 'NIL'
    ptext_6    = Paragraph(ptext6,styles['Justify'])
    word =''

    word = word + '<br/><br/><font size=11><b>%s <br/>%s</b></font><br/>'
    word = word % (owner, NRIC)
    word = 'Name:'+word+'<br/>Address:<br/> '+'<br/><b> %s<br/></b>'
    word = word %(owner_address)
    ptext_10 = Paragraph(word,styles['Justify'])
    the_property_description ='<font size=11>Postal Address: <br/><br/><b>%s</b><br/><br/><br/>Description: <b>%s</b><br/><br/><br/>Held under Title (if individual title has been issued):<br/><br/><br/><b>%s</b><br/><br/>Built thereon Master Title (if individual title has not been issued):<br/><br/></font>'
    the_property_description = the_property_description %(sold_house_address,property_description,house_title)
    if master_title!='':
        the_property_description = the_property_description +'<b>%s</b>'
        the_property_description = the_property_description %master_title
    the_property_description     =  Paragraph(the_property_description,styles['Justify'])
    able = [[ptext, "", ptext_11 ], [ptext_1, "Date of Agreement", " "], [ptext_2, "Vendor", ptext_10], [ptext_3, 'Property', the_property_description],
            [ptext_4,ptext_5 , ptext_6]]
    t    = Table(able, (2.5* cm, 5 * cm, 7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(PageBreak())
    ptext = "<font size=11><u>Schedule 2</u></font>"
    Story.append(Paragraph(ptext, styles['title']))
    Story.append(Spacer(1, 11))
    ptext1     = "<font size=11><b>Item</b></font>"
    ptext_1    = Paragraph(ptext1,styles['Title'])
    ptext2     = "<font size=11><b>Particulars</b></font>"
    ptext_2    =  Paragraph(ptext2,styles['Title'])
    ptext3     = "<font size=11><b>2A</b></font>"
    ptext_3    = Paragraph(ptext3, styles['Title'])
    ptext4     = "<font size=11><b>2B</b></font>"
    ptext_4    = Paragraph(ptext4, styles['Title'])
    theword    = num2words(float(agreed_price))
    word_upper = theword.title()
    new_price  = "RM{:,.2f}".format(int(agreed_price))
    ptext5     = "<font size=10>%s<br/><br/> (Ringgit Malaysia: %s only)</font>"
    ptext5     = ptext5 % (new_price,word_upper)
    ptext_5    = Paragraph(ptext5, styles['Normal'])
    ptext6     = "<font size=10>Date: </font>"
    ptext_6    = Paragraph(ptext6, styles['Normal'])
    able       = [[ptext_1,'',ptext_2],[ptext_3,'Purchase Price',ptext_5],[ptext_4,'Completion Date',ptext_6]]
    t          = Table(able, (2.5 * cm, 5 * cm, 7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)


    doc.build(Story, canvasmaker=PageNumCanvas)
