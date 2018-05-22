import requests, json, pprint
from itertools import izip
import random, time
from random import randint
"""
composer participant add 
-c admin@one-network -d 
'{"$class":"org.acme.model.owner",
"ownerID":"owner01",
"nric":"owner_01_960122106187", 
"firstName":"Mike","lastName":"Leow", 
"email_address":"leowyennhan@gmail.com", 
"type_of_employee":"self_employed",
"income_amount":168888888,"ccris_score":3,"ctos_score":2}'
"""
'''
def read_data():
    filename1="test.txt"
    filename3="ic_gen.txt"
    filename4="owner_id.txt"
    filename2="email.txt"
    the_list= []
    full_list = []
    names=[]
    numbers=[]
    NRIC=[]
    owner_id=[]
    email=[]
    data_tryout={}
    with open(filename1) as f1,open(filename2) as f2,open(filename3) as f3,open(filename4) as f4:
        i=0
        for line1,line2,line3,line4 in izip(f1,f2,f3,f4):
            for value1,value2,value3,value4 in izip(line1.split(),line2.split(),line3.split(),line4.split()):
                names.append(value1)
                email.append(value2)
                NRIC.append(value3)
                owner_id.append(value4)

    x=0
    y=0
    z=0

    employee_status=["self_employed","employee","student"]
    random_amount_income=[162166,423845,182032,721978,614494,844511,577362,251809,153249,337235,94635,999129,529582,614147,242437,639180,264369,423368,263152,511885]
    random_scores=[0,1,2,3,4,5]
    for x in range(100):
        the_list.append(names[x])
        z+=1
        if z==2:
            z=0
            the_list.insert(0,owner_id[y])
            the_list.insert(0,NRIC[y])
            the_list.append(email[y])
            the_list.append(random.choice(employee_status))
            the_list.append(random.choice(random_amount_income))
            the_list.append(random.choice(random_scores))
            the_list.append(random.choice(random_scores))
            the_list.insert(0,"org.acme.model.owner")
            y+=1
            full_list.append(the_list)
            the_list=[]
    return(full_list)
'''
def write_file():
    file = open("owner_id.txt",'w')
    for i in range(1,101):
        file.write("owner"+str(i)+'\n')
    file.close()

def write_to_sample(full_list):
    file = open("sample_of_50.txt",'w')
    for i in full_list:
        for item in i:
            file.write(str(item)+" ")
        file.write('\n')
    file.close()
def write_to_owner():
    list = []
    the_list = []
    filename1 = "sample_of_50.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)
            the_list.append(list)
            list = []
    data={}
    for i in range(len(the_list)):
        data['ownerID']=the_list[i][2]
        data['nric'] = the_list[i][1]
        data['firstName']=the_list[i][3]
        data['lastName']=the_list[i][4]
        data['email_address']=the_list[i][5]
        data['type_of_employee']=the_list[i][6]
        data['income_amount']=the_list[i][7]
        data['ccris_score']=the_list[i][8]
        data['ctos_score']=the_list[i][9]
        dump_data_owner(data)



def dump_data_owner(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(owner_id, json=data, headers=headers)
    pprint.pprint(response.json())


def write_land_title():
    states=["Wilayah","PENANG","SELANGOR","PERAK","JOHOR","SABAH","SARAWAK","MELAKA","KEDAH","TERENGGANU","PAHANG","KELANTAN","NEGERI_SEMBILAN","PERLIS"]
    cukai_tahunan=[30,50,70,90,120,150,140,175,123,128,198,188,588,888]
    johor=["Daerah_Batu_Pahat","Johor_Bahru","Kluang","Daerah_Kota_Tinggi","Kulai","Daerah_Mersing","Daerah_Muar","Daerah_Pontian","Daerah_Segamat","Tangkak"]
    kedah=["Daerah_Baling","Daerah_Bandar_Baharu","Kota_Setar","Kuala_Muda","Kubang_Pasu","Kulim","Langkawi","Padang_Terap","Pendang","Pokok_Sena","Sik","Yan"]
    kelantan=["Bachok","Gua_Musang","Jeli","Kota_Bahru","Kuala_Krai","Machang","Pasir_Mas","Pasir_Puteh","Tanah_Merah","Tumpat","Lojing"]
    melaka=["Alor_Gajah","Melaka_Tengah","Jasin"]
    n9=["Jelebu","Jempol","Kuala_Pilah","Port_Dickson","Rembau","Seremban","Tampin"]
    pahang=["Bentong","Bera","Cameron_Highland","Jerantut","Kuantan","Lipis","Maran","Pekan","Raub","Rompin","Termeloh"]
    penang=["Timur_Laut","Barat_Daya","Seberang_Perai_Utara","Seberang_Perai_Tengah","Seberang_Perai_Selatan"]
    perak=["Batang_Padang","Hilir_Perak","Hulu_Perak","Kampar","Kerian","Kinta","Kuala_Kangsar","Larut, Matang_dan_Selama","Manjung","Muallim","Perak_Tengah","Daerah_Bagan_Datuk"]
    perlis="Perlis"
    selangor=["Gombak","Hulu_Langat","Hulu_Selangor","Klang","Kuala_Langat","Kuala_Selangor","Petaling","Sabak_Bernam","Sepang"]
    terengganu=["Besut","Dungun","Hulu_Terengganu","Keamanan","Kuala_Terengganu","Marang","Setiu","Kuala_Nerus"]
    wilayah=["Kuala_Lumpur","Labuan","Putrajaya"]
    sabah=["kudat","pantai_barat","pedalaman","sandakan","tawau"]
    sarawak=["betong","bintulu","kapit","kuching","limbang","miri","mukah","samarahan","sarikei","serian","sibu","sri_aman"]
    kategori_tanah=["Tiada","Bangunan","Pertanian","Tanah"]
    type_of_location=["Bandar","Pekan","Mukim"]
    no_lot=["LOT_01A","LOT_20B","LOT_875","LOT_69C","LOT_44B","LOT_88A","LOT_90E"]
    luas_lot=["24306.3928","12,7222,0000","1.2646","139","140","250"]
    lembaran_piawai=["111-C","109-C","110-C"]
    luas_format="Meter Persegi"

    file = open("asset_of_50_land_title.txt",'w')
    for i in range(51):
        the_state = random.choice(states)
        if the_state == "Wilayah":
            daerah = random.choice(wilayah)
        elif the_state == "PENANG":
            daerah = random.choice(penang)
        elif the_state == "SELANGOR":
            daerah = random.choice(selangor)
        elif the_state == "PERAK":
            daerah = random.choice(perak)
        elif the_state == "JOHOR":
            daerah = random.choice(johor)
        elif the_state == "SABAH":
            daerah = random.choice(sabah)
        elif the_state == "SARAWAK":
            daerah = random.choice(sarawak)
        elif the_state == "MELAKA":
            daerah = random.choice(melaka)
        elif the_state == "KEDAH":
            daerah = random.choice(kedah)
        elif the_state == "TERENGGANU":
            daerah = random.choice(terengganu)
        elif the_state == "PAHANG":
            daerah = random.choice(pahang)
        elif the_state == "KELANTAN":
            daerah = random.choice(kelantan)
        elif the_state == "NEGERI_SEMBILAN":
            daerah = random.choice(n9)
        elif the_state == "PERLIS":
            daerah = "perlis"
        cukai=random.choice(cukai_tahunan)
        number_lot=random.choice(no_lot)
        location_type=random.choice(type_of_location)
        luas1= random.choice(luas_lot)
        categori=random.choice(kategori_tanah)
        lembaran=random.choice(lembaran_piawai)
        file.write("resource:org.acme.model.""owner#owner"+str(i)+" "+"land"+str(i)+" "+str(cukai)+" "+str(the_state)+" "+str(daerah)+" "+str(location_type)+" "+str(number_lot)+" "+str(luas1)+" "+categori+" "+ lembaran)
        file.write('\n')
    file.close()

def read_data():
    list=[]
    the_list=[]
    filename1="asset_of_50_land_title.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)
            the_list.append(list)
            list=[]
    return the_list
'''
{
  "$class": "org.acme.model.Bank",
  "bankID": "0107",
  "bank_name": "",
  "bankerID": "",
  "bank_address": {
    "$class": "org.acme.model.Address"
  }
}'''

def write_bank_id():
    bank_names=['Maybank','Bank Rakyat','UOB','RHB','HongLeong','Standard Chartered','HSBC','Affin','CIMB','Ambank','Citibank','Alliance Bank','Public Bank']
    file = open("asset_of_banks.txt", 'w')
    streets=["100 Jalan Tun Perak ","No.33, Jalan Rakyat","Jalan Raja Laut ","Jalan Tun Razak","6 Jalan Damanlela,Bukit Damansara","No. 30, Jalan Sultan Ismail","No 2 Leboh Ampang","80, Jalan Raja Chulan","Jalan Stesen Sentral 2","No. 8, Jalan Yap Kwan Seng","165 Jalan Ampang","No.8, Jalan Munshi Abdullah","146 Jalan Ampang"]
    postal_code=["50050","50470","50738","50400","50490","50250","50100","53300","50740","50450","50754","50100","50450"]
    p_o_box=["11057","11024","11212","10145","10510","unknown","10244","202","11751","10922","11725","163","12542"]
    data={}
    o={}
    for i in range(len(bank_names)):
        data["bankID"] = "bank"+str(i)
        data["bank_name"] = bank_names[i]
        data["bankerID"] = "banker"+str(i)
        data["bank_address"] = {"city":"Kuala Lumpur","country":"Malaysia","locality":"City","region":"SEA","street":streets[i],"postalCode":postal_code[i],"postOfficeBoxNumber":p_o_box[i]}
        dumb_data_bank(data)


def dumb_data_bank(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(bank_id, json=data, headers=headers)
    pprint.pprint(response.json())
''''{
  "$class": "org.acme.model.company",
  "companyID": "string",
  "company_name": "string",
  "employee_in_this_company_ID": {},
  "company_category": []
}'''
def write_company():
    data={}
    companies=["yilou","Prada","Shell","Petronas","PosLaju","Pizza_Hut","BestDengki","BMW","Mercedes","Toyota","Pemanis","Honda","CottonOn","Jibby&Co","Yahoo","Starbucks","IT_Solution","BCG","Exxon_Mobile","Accenture"]
    category=["F&B","Retail","Services","Services","Logistics","F&B","Eletronics","Automotives","Automotives","Automotives","F&B","Automotives","Retail&Fashion","F&B","MSC","F&B-Franchise","Consulting","Consulting","Oil&Gas","IT_solution"]
    for i in range(20):
        data["companyID"] = "company"+str(i)
        data["company_name"] = companies[i]
        data["employee_in_this_company_ID"] =[]
        a= "resource:org.acme.model.""owner#owner"+str(i)
        data["employee_in_this_company_ID"].append(a)
        data["company_category"] = [category[i]]
        dump_data_company(data)
def add_lawyer_company():
    data={}
    company=["Rahayu Partnership","HS LIM & CO","Donovan & Ho","JK Lim Advocates & Solicitors","Mirandah Asia","MahWengKwai & Associates"]
    a=20
    for i in range(len(company)):
        data["companyID"] = "company"+str(a)
        data["company_name"] = company[i]
        data["employee_in_this_company_ID"] = "resource:org.acme.model.""owner#owner" + str(a)
        data["company_category"]=["Law Firm"]
        a+=1
        dump_data_company(data)

'''
  "$class": "org.acme.model.Lawyer",
  "lawfirmID": "string",
  "lawyer_firm_id": {},
  "lawyer_id": "string",
  "company_lawyer_name": "string"
'''
def add_lawyer_participant():
    data={}
    company=["Rahayu_Partnership","HS_LIM_&_CO","Donovan_&_Ho","JK_Lim_Advocates_&_Solicitors","Mirandah_Asia","MahWengKwai_&_Associates"]
    a=20
    for i in range(len(company)):
        data["lawfirmID"]="lawfirm"+str(i)
        data["lawyer_firm_id"] = "resource:org.acme.model.""company#company"+str(a)
        data["lawyer_id"] = company[i]+"_lawyer_"+str(i)
        data["company_lawyer_name"] = company[i]
        a+=1
        dump_data_lawyer(data)

def dump_data_lawyer(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(lawyer_id, json=data, headers=headers)
    pprint.pprint(response.json())

def dump_data_company(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(company_id, json=data, headers=headers)
#land title fake data dumping.
def convert_to_json_land():
    data={}
    list = []
    the_list = []
    filename1 = "asset_of_50_land_title.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)
            the_list.append(list)
            list = []
    for i in range(len(the_list)):
        data["ownerid"]          = (the_list[i][0])
        data["hakmilik_id"]         = (the_list[i][1])
        data["cukai_tahunan"]            = (the_list[i][2])
        data['Negeri']       = (the_list[i][3])
        data['Daerah']        = (the_list[i][4])
        data['location_type']   = (the_list[i][5])
        data['no_lot']= (the_list[i][6])
        data['luas_lot']   = (the_list[i][7])
        data['kategori_tanah']     = (the_list[i][8])
        data['daftaran_pada']      = time.asctime( time.localtime(time.time()) )
        data['no_lembaran_piawai'] = (the_list[i][9])
        dumb_data(data)
        #print(data)

def dumb_data(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(land_title, json=data, headers=headers)
    pprint.pprint(response.json())


data ={}
#write_file()
write_land_title()
the_list= read_data()
write_bank_id()
convert_to_json_land()
write_company()
add_lawyer_company()
add_lawyer_participant()
write_to_owner()
