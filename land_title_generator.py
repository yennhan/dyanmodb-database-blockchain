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

def land_title_pdf_generator(name,land_id,cukai_tahunan,negeri,daerah,bandar,tempat,lot_no,luas_lot,land_usage,pelembaran_piawai,permohonan_ukur,fail_number,time,tarik_pemberi,previous_owner_id,NRIC):
    doc = SimpleDocTemplate(land_id + ".pdf", rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('Center', alignment=TA_LEFT, leftIndent=20))
    styles.add(ParagraphStyle('one', alignment=TA_LEFT, leftIndent=10))
    styles.add(ParagraphStyle('two', alignment=TA_JUSTIFY, leftIndent=100))
    styles.add(ParagraphStyle('t1', alignment=TA_JUSTIFY, leftIndent=20))
    styles.add(ParagraphStyle('left', alignment=TA_LEFT))
    Story = []
    ptext='Kanun Tanah Negara'
    ptext3=Paragraph(ptext,styles['Title'])
    ptext1 = '<font size=15><b>BORANG 11BK<br/><br/>(Jadual Keempat Belas)</b></font>'
    ptext_1 = Paragraph(ptext1, styles['Title'])
    ptext2='<font size=10><b>GERAN</b></font>'
    ptext_2 = Paragraph(ptext2,styles['Title'])
    able = [['',ptext3, ''],
            ['', ptext_1, ''], ['', ptext_2, '']]
    t = Table(able, (2.5 * cm, 12 * cm, 2.5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    ptext="<font size=11><br/>No H.S.(M)<br/><br/></font>"
    ptext1= Paragraph(ptext,styles['left'])
    ptext2="<font size=11><br/>Cukai Tahunan : RM%s<br/><br/></font>" %cukai_tahunan
    ptext_2= Paragraph(ptext2,styles['left'])
    able=[[ptext1,ptext_2]]
    t = Table(able,(10 * cm, 10 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext1  ="Negeri "
    ptext2  ="%s" %negeri
    ptext_1 = Paragraph(ptext1,styles['one'])
    ptext_2 = Paragraph(ptext2,styles['left'])
    ptext3  = "Daerah "
    ptext4  = "%s" % daerah
    ptext_3 = Paragraph(ptext3, styles['one'])
    ptext_4 = Paragraph(ptext4, styles['left'])
    ptext5  = "Bandar/Pekan/Mukim/Country "
    ptext6  = "%s" % bandar
    ptext_5 = Paragraph(ptext5, styles['one'])
    ptext_6 = Paragraph(ptext6, styles['left'])
    ptext7 = "Tempat"
    ptext8 = "%s" % tempat
    ptext_7 = Paragraph(ptext7, styles['one'])
    ptext_8 = Paragraph(ptext8, styles['left'])
    ptext9 = "No. PT"
    ptext10 = "%s" % lot_no
    ptext_9 = Paragraph(ptext9, styles['one'])
    ptext_10 = Paragraph(ptext10, styles['left'])
    ptext11 = "Luas Sementara"
    ptext12 = "%s Meter Persegi"% luas_lot
    ptext_11 = Paragraph(ptext11, styles['one'])
    ptext_12 = Paragraph(ptext12, styles['left'])
    ptext13 = "Kategori Pengunaan Tanah"
    ptext14 = "%s" % land_usage
    ptext_13 = Paragraph(ptext13, styles['one'])
    ptext_14= Paragraph(ptext14, styles['left'])
    ptext15 = "No. Lembaran Piawai"
    ptext16="%s" % pelembaran_piawai
    ptext_15 = Paragraph(ptext15, styles['one'])
    ptext_16 = Paragraph(ptext16, styles['left'])
    ptext17 = "No. Permohonan Ukur"
    ptext18 = "%s" % permohonan_ukur
    ptext_17 = Paragraph(ptext17, styles['one'])
    ptext_18 = Paragraph(ptext18, styles['left'])
    ptext19 = "No. Fail"
    ptext20 = "%s" % fail_number
    ptext_19 = Paragraph(ptext19, styles['one'])
    ptext_20 = Paragraph(ptext20, styles['left'])
    able = [[ptext_1,':', ptext_2],[ptext_3,":",ptext_4],[ptext_5,':',ptext_6],
            [ptext_7,":",ptext_8],[ptext_9,":",ptext_10],[ptext_11,':',ptext_12],
            [ptext_13,":",ptext_14],[ptext_15,":",ptext_16],[ptext_17,":",ptext_18],[ptext_19,":",ptext_20]]
    t = Table(able, (6 * cm,1*cm, 6 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    ptext="Geran untuk selama-lamanya"
    ptext1= Paragraph(ptext,styles['Justify'])
    Story.append(ptext1)
    Story.append(Spacer(1, 11))
    ptext = "Didaftarkan pada <br/>%s" %time
    ptext1 = Paragraph(ptext, styles['Justify'])
    ptext3= ".........................<br/><br/>Pendaftar"
    ptext_3 = Paragraph(ptext3,styles['two'])
    ptext2 = "Document hakmilik keluaran dikeluarkan pada <br/>%s" % time
    ptext_2 = Paragraph(ptext2, styles['Justify'])
    ptext4 = ".........................<br/><br/>Pendaftar"
    ptext_4= Paragraph(ptext4,styles['two'])
    able = [[ptext1,ptext_3],[ptext_2,ptext_4]]
    t = Table(able, (7 * cm, 7 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    Story.append(PageBreak())
    ptext = "Pelan tanah, bagi maksud pengenalan, adalah dikepikan pada Borang B1."
    ptext_1= Paragraph(ptext,styles['Justify'])
    Story.append(ptext_1)
    ptext= "<font size=9><b>SYARAT-SYARAT NYATA</b></font>"
    ptext_1= Paragraph(ptext,styles['Title'])
    ptext2="<font size=9>(FIRST GRADE)</font>"
    ptext_2 = Paragraph(ptext2,styles['left'])
    ptext3 = "<font size=9>The Land comprised in this title:<br/> (a) shall not be affected by any provision of the National Land Code limiting the compensation payable on the exercise by the State Authority of a right of access or use conferred by Chapter 3 of Part Three of the Code or on the creation of a Land Adminstrator's right of way;<br/> and<br/>(b) subject to the implied condition that land is liable to be re-entered if it is abandoned for more than three years shall revert to the State only if the proprietor for the time being dies without heirs; <br/><br/> and the title shall confer the absolute right to all foret produce and to all oil, mineral and other natural deposits on or below the surface of the land(including the right to work or extract any such produce or deposits and remove it beyond the boundaries of the land)</font>"
    ptext_3 = Paragraph(ptext3, styles['left'])
    ptext4 = "<font size=9><b>SEKATAN-SEKATAN KEPENTINGAN</b><br/>Tiada</font>"
    ptext_4 = Paragraph(ptext4,styles['Title'])
    able = [['', ptext_1, ''],['',ptext_2,''],['',ptext_3,''],['','',''],['',ptext_4,'']]
    t = Table(able, (5*cm, 9 * cm, 5 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
         #('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
         #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    line = MCLine(400)
    Story.append(line)
    ptext='<font size=9><i>Hendaklah dipenuhkan apabila hakmilik dikeluarkan bagi sambungan</i></font>'
    ptext_1 = Paragraph(ptext,styles['Center'])
    Story.append(ptext_1)
    Story.append(Spacer(1, 11))
    ptext='<font size=9>Tarik mula-mula pemberimilikan</font>'
    ptext_1 = Paragraph(ptext, styles['Justify'])
    ptext2 = ': %s ' % tarik_pemberi
    ptext_2 = Paragraph(ptext2,styles['Justify'])
    ptext3 = '<font size=9>No. hakmilik asal (Tetap atau sementara)</font>'
    ptext_3 = Paragraph(ptext3, styles['Justify'])
    ptext4 = ':'
    ptext_4 = Paragraph(ptext4, styles['Justify'])
    ptext5 = '<font size=9>No. hakmilik yang terdahulu daripada ini <br/><i>(jika berlainan daripada di atas)</i></font>'
    ptext_5 = Paragraph(ptext5, styles['Justify'])
    ptext6 = '<font size=9>: %s</font>' %previous_owner_id
    ptext_6 = Paragraph(ptext6, styles['Justify'])
    able=[[ptext_1,ptext_2,''],[ptext_3,ptext_4,''],[ptext_5,ptext_6,'']]
    t = Table(able, (7 * cm, 5 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        #('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    line = MCLine(400)
    Story.append(line)
    ptext='<font size=9><b>REKOD KETUANPUNYAAN</b></font>'
    ptext_1 = Paragraph(ptext,styles['Title'])
    Story.append(ptext_1)
    ptext='%s, NO K/P Baru: %s, Warganegara Malaysia' %(name,NRIC)
    ptext_1= Paragraph(ptext,styles['Justify'])
    able=[[ptext_1,'','']]
    t = Table(able, (7 * cm, 5 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    ptext = '<font size=9><b>REKOD URUSANN</b></font>'
    ptext_1 = Paragraph(ptext, styles['Title'])
    Story.append(ptext_1)
    Story.append(Spacer(1, 11))
    ptext = '<font size=9><b>PERKARA LAIN YANG MELIBATKAN HAKMILIK</b></font>'
    ptext_1 = Paragraph(ptext, styles['Title'])
    Story.append(ptext_1)
    ptext = '<font size=9><b>...............<br/>Pendaftar</b></font>'
    ptext_1 = Paragraph(ptext, styles['Title'])
    able = [['', '', ptext_1]]
    t = Table(able, (7 * cm, 5 * cm, 3 * cm))
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('INNERGRID', (0, 0), (-1, -1), 1.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('BOX', (0, 0), (-1, -1), 1.50, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 11))
    Story.append(Spacer(1, 11))
    line = MCLine(400)
    Story.append(line)
    doc.multiBuild(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


cukai_tahunan="460"
land_id="land5"
negeri="SELANGOR"
daerah="PETALING"
bandar="GOMBAK"
tempat="OFF JALAN KERAMAT HUJONG"
lot_no="LOT 5071"
luas_lot="1005"
land_usage="Bangunan"
pelembaran_piawai=""
permohonan_ukur=""
fail_number="PHT. KL. 6/495/61"
time1 = time.asctime(time.localtime(time.time()))
tarik_pemberi=time.asctime(time.localtime(time.time()))
previous_owner_id="HSD 23029 Mukim 12"
NRIC="9601211-13-6100"
#land_title_pdf_generator(land_id,cukai_tahunan,negeri,daerah,bandar,tempat,lot_no,luas_lot,land_usage,pelembaran_piawai,permohonan_ukur,fail_number,time1,tarik_pemberi,previous_owner_id,NRIC)