# coding=utf-8
#Leow Yenn Han
#leowyennhan@gmail.com
import time
from flask import Flask, render_template , request, make_response, Blueprint
from flask_bootstrap import Bootstrap
import requests, json, pprint
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table,TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.lib.units import inch
from reportlab.lib.units import cm,mm
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from num2words import num2words
import io

class MCLine(Flowable):
    """
    Line flowable --- draws a line in a flowable
    http://two.pairlist.net/pipermail/reportlab-users/2005-February/003695.html
    """

    # ----------------------------------------------------------------------
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    # ----------------------------------------------------------------------
    def __repr__(self):
        return "Line(w=%s)" % self.width

    # ----------------------------------------------------------------------
    def draw(self):
        """
        draw the line
        """
        self.canv.line(0, self.height, self.width, self.height)


# ----------------------------------------------------------------------
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


def invoice_pdf_generator(logo_im,invoice_id,company_name,company_address,purchaser,time1,the_list):
    doc = SimpleDocTemplate(invoice_id + ".pdf", rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('Center', alignment=TA_LEFT, leftIndent=130))
    styles.add(ParagraphStyle('one', alignment=TA_RIGHT, rightIndent=20))
    styles.add(ParagraphStyle('two', alignment=TA_JUSTIFY, leftIndent=300))
    styles.add(ParagraphStyle('t1', alignment=TA_JUSTIFY, leftIndent=200))
    styles.add(ParagraphStyle('left', alignment=TA_LEFT))
    logo = logo_im
    im = Image(logo, 1.3 * inch, 1 * inch)
    Story = []
    ptext = '<font size=12>Supplier Name:<br/><b> %s</b><br/></font>' % company_name
    ptext_1 = Paragraph(ptext, styles['left'])
    ptext2='<font size=9>%s</font>' %company_address
    ptext_2 = Paragraph(ptext2,styles['left'])
    ptext5='<font size=9><b>Shipment To:</b><br/>%s</font>'%company_address
    ptext_5= Paragraph(ptext5,styles['left'])
    if purchaser=="":
        ptext3 = "<font size=9><b>Bill:</b><br/>Cash</font>"
        ptext_3 = Paragraph(ptext3, styles['left'])
    else:
        ptext3 = "<font size=9><b>Bill To</b><br/>%s</font>" % purchaser
        ptext_3 = Paragraph(ptext3, styles['left'])
    ptext4="<font size=9><b>Invoice#   </b>     %s<br/><b>Invoice Date of Issue:  </b> %s<br/></font>" %(invoice_id,time1)
    ptext_4= Paragraph(ptext4,styles['left'])
    able = [['','',im],[ptext_1, '', ''],[ptext_2,'',''],['','',''],[ptext_3,'',ptext_4],[ptext_5,'','']]
    t = Table(able, (5* cm, 7 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         #('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    line = MCLine(440)
    Story.append(line)
    Story.append(Spacer(1, 11))
    Story.append(line)
    Story.append(Spacer(1, 11))
    able=[['QTY','DESCRIPTION','UNIT PRICE','AMOUNT (RM) ']]
    t = Table(able, (2 * cm, 7.5 * cm, 3 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
         ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
    ]))
    Story.append(t)
    value=0
    for item in the_list:
        value+=item['amount']
        p1=str(item['qty'])
        p2=item['description_of_item']
        p3=str(item['unit_price'])
        p4=str(item['amount'])
        p_1= Paragraph(p1,styles['one'])
        p_2 = Paragraph(p2, styles['one'])
        p_3 = Paragraph(p3, styles['one'])
        p_4 = Paragraph(p4, styles['one'])
        able = [[p_1, p_2, p_3, p_4]]
        t = Table(able, (2 * cm, 7.5 * cm, 3 * cm, 3 * cm))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        Story.append(t)
    gst=value*0.06
    total=value+gst
    t1=str(value)
    t_1=Paragraph(t1,styles['one'])
    t2=str(gst)
    t_2=Paragraph(t2,styles['one'])
    t3=str(total)
    t_3=Paragraph(t3,styles['one'])
    ptext="<font size=9>Subtotal</font>"
    ptext_1=Paragraph(ptext,styles['two'])
    ptext1 = "<font size=9>GST</font>"
    ptext_2 = Paragraph(ptext1, styles['two'])
    ptext2="<font size=9><b>TOTAL</b></font>"
    ptext_3 = Paragraph(ptext2,styles['two'])
    able=[[ptext_1,t_1],[ptext_2,t_2],[ptext_3,t_3]]
    t = Table(able, ( 12.5* cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (1, 0), (1,2), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (1,0), (1, 2), 0.5, colors.black)
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(line)
    Story.append(Spacer(1, 11))
    ptext="<font size=9>All taxable products & services at GST @ 6%</font>"
    ptext1= Paragraph(ptext,styles['Center'])
    Story.append(ptext1)
    ptext='<font size=9>Thank You</font>'
    ptext1= Paragraph(ptext,styles['t1'])
    Story.append(ptext1)
    ptext = '<font size=9>**************** Official Invoice ****************</font>'
    ptext1 = Paragraph(ptext, styles['Center'])
    Story.append(ptext1)
    Story.append(Spacer(1, 11))
    Story.append(line)
    doc.multiBuild(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


#purchaser="Jibby&Co"
#time1=time.asctime(time.localtime(time.time()))

#the_list=[{"qty":3,"description_of_item":"LENOVO 15inch Laptop","unit_price":5000,"amount":15000},{"qty":4,"description_of_item":"Dell 15inch Laptop","unit_price":2000,"amount":8000}]
#invoice_pdf_generator("test","Best Dengki Sdn Bhd","455, Amsterdam Avenue<br/>Petaling Jaya, 47400,<br/> Selangor Dahrul Ehsan",purchaser,time1,the_list)