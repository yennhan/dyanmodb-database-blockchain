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

def profit_loss_pdf(pdf_name,company_name,company_address,revenue,cost_of_goods,total_salary,rental,office_supply,insurance,utilities,maintanence,telecommunication):
    doc = SimpleDocTemplate(pdf_name, rightMargin=72, leftMargin=72,
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
    line = MCLine(410)
    logo = "jibby.png"
    im = Image(logo, 1.3 * inch, 1 * inch)
    Story = []
    ptext = '<font size=10><b>%s</b><br/>%s</font>' % (company_name,company_address)
    ptext_1 = Paragraph(ptext, styles['left'])

    able = [[ptext_1,'', im], ['', '', ''], ['', '', '']]
    t = Table(able, (5 * cm, 7 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    ptext3 = '<font size=13><b><u>Profit & Loss Statement for Jibby and Co</u></b></font>'
    ptext_3 = Paragraph(ptext3, styles['left'])
    Story.append(ptext_3)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext1 = '<font size=11><b>Total Revenue</b></font>'
    ptext_1 = Paragraph(ptext1, styles['left'])
    ptext2 = '<font size=10>%s</font>' % str("{:,}".format(revenue))
    ptext_2 = Paragraph(ptext2, styles['one'])
    ptext4 = '<font size=11>Cost of Goods Sold</font>'
    ptext_4 = Paragraph(ptext4, styles['left'])
    ptext3 = '<font size=10>(%s)</font>' % str("{:,}".format(cost_of_goods))
    ptext_3 = Paragraph(ptext3, styles['one'])
    able = [[ptext_1, '', ptext_2],[ptext_4,'',ptext_3],['','','']]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(line)
    gross_profit = revenue - cost_of_goods
    ptext = '<font size=11><b>Gross Profit </b></font>'
    ptext_1 = Paragraph(ptext, styles['left'])
    ptext2 = '<font size=10>%s</font>' % str("{:,}".format(gross_profit))
    ptext_2 = Paragraph(ptext2, styles['one'])
    able = [[ptext_1, '', ptext_2]]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(line)
    ptext5='<font size=11><b>Operating Expenses</b></font>'
    ptext_5 = Paragraph(ptext5, styles['left'])
    ptext6 = '<font size=10>Salaries, Benefit and Wages</font>'
    ptext_6 = Paragraph(ptext6, styles['left'])
    ptext7 = '<font size=10>(%s)</font>' % str("{:,}".format(total_salary))
    ptext_7 = Paragraph(ptext7, styles['one'])
    ptext8 = '<font size=10>Rent</font>'
    ptext_8 = Paragraph(ptext8, styles['left'])
    ptext9 = '<font size=10>(%s)</font>' % str("{:,}".format(rental))
    ptext_9 = Paragraph(ptext9, styles['one'])
    ptext10 = '<font size=10>Office Supplies</font>'
    ptext_10 = Paragraph(ptext10, styles['left'])
    ptext11 = '<font size=10>(%s)</font>' % str("{:,}".format(office_supply))
    ptext_11 = Paragraph(ptext11, styles['one'])
    ptext12 = '<font size=10>Insurance </font>'
    ptext_12 = Paragraph(ptext12, styles['left'])
    ptext13 = '<font size=10>(%s)</font>' % str("{:,}".format(insurance))
    ptext_13 = Paragraph(ptext13, styles['one'])
    ptext14 = '<font size=10>Utilities </font>'
    ptext_14 = Paragraph(ptext14, styles['left'])
    ptext15 = '<font size=10>(%s)</font>' % str("{:,}".format(utilities))
    ptext_15 = Paragraph(ptext15, styles['one'])
    ptext16 = '<font size=10>Maintanence </font>'
    ptext_16 = Paragraph(ptext16, styles['left'])
    ptext17 = '<font size=10>(%s)</font>' % str("{:,}".format(maintanence))
    ptext_17 = Paragraph(ptext17, styles['one'])
    ptext18 = '<font size=10>Telecommunication </font>'
    ptext_18 = Paragraph(ptext18, styles['left'])
    ptext19 = '<font size=10>(%s)</font>' % str("{:,}".format(telecommunication))
    ptext_19 = Paragraph(ptext19, styles['one'])
    able = [['','',''],[ptext_5,'',''],[ptext_6,'',ptext_7],
            [ptext_8,'',ptext_9  ],[ptext_10,'',ptext_11],
            [ptext_12,'',ptext_13],[ptext_14,'',ptext_15],
            [ptext_16,'',ptext_17],[ptext_18,'',ptext_19]]
    t = Table(able, (8* cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(line)
    total_expenses = total_salary + rental + office_supply + insurance + utilities + maintanence + telecommunication
    ptext='<font size=11>Total Expenses</font>'
    ptext_1=Paragraph(ptext,styles['left'])
    ptext2 = '<font size=10>(%s)</font>' %str("{:,}".format(total_expenses))
    ptext_2 = Paragraph(ptext2, styles['one'])
    able = [[ptext_1, '', ptext_2]]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(line)
    profit_before_tax = gross_profit - total_expenses
    ptext = '<font size=11><b>Profit Before Tax </b></font>'
    ptext_1 = Paragraph(ptext, styles['left'])
    ptext2 = '<font size=10>%s</font>' % str("{:,}".format(profit_before_tax))
    ptext_2 = Paragraph(ptext2, styles['one'])
    able = [[ptext_1, '', ptext_2]]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    income_tax = int(profit_before_tax*0.19)
    ptext = '<font size=10>Income Taxes </font>'
    ptext_1 = Paragraph(ptext, styles['left'])
    ptext2 = '<font size=10>%s</font>' % str("{:,}".format(income_tax))
    ptext_2 = Paragraph(ptext2, styles['one'])
    able = [[ptext_1, '', ptext_2]]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(line)
    net_profit=profit_before_tax-income_tax
    ptext = '<font size=10><b>Net Profit</b> </font>'
    ptext_1 = Paragraph(ptext, styles['left'])
    ptext2 = '<font size=10>%s</font>' % str("{:,}".format(net_profit))
    ptext_2 = Paragraph(ptext2, styles['one'])
    able = [[ptext_1, '', ptext_2]]
    t = Table(able, (8 * cm, 2 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
    ]))
    Story.append(t)
    Story.append(line)
    doc.multiBuild(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


company_name='Jibby & Co'
company_address= "Empire Shopping Gallery, Jalan SS 16/1, Ss 16, 47500 Subang Jaya, Selangor"
revenue=150000
cost_of_goods=40000
total_salary=10000
rental=20000
office_supply=100
insurance=3000
utilities=1500
maintanence=700
telecommunication=300
#profit_loss_pdf(company_name,company_address,revenue,cost_of_goods,total_salary,rental,office_supply,insurance,utilities,maintanence,telecommunication)