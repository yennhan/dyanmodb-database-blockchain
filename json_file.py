import requests, json, pprint

def read_data():
    list=[]
    the_list=[]
    filename1="sample_of_50.txt"
    with open(filename1) as f1:
        for line1 in f1:
            for item in line1.split():
                list.append(item)

            the_list.append(list)
            list=[]
    return the_list
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

def convert_to_json(the_list):
    data={}
    for i in range(len(the_list)):
        data["$class"]          = (the_list[i][0])
        data["nric"]         = (the_list[i][1])
        data['ownerID']            = (the_list[i][2])
        data['firstName']       = (the_list[i][3])
        data['lastName']        = (the_list[i][4])
        data['email_address']   = (the_list[i][5])
        data['type_of_employee']= (the_list[i][6])
        data['income_amount']   = (the_list[i][7])
        data['ccris_score']     = (the_list[i][8])
        data['ctos_score']      = (the_list[i][9])
        #dumb_data(data)


def dumb_data(data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(owner_post, json=data, headers=headers)
    pprint.pprint(response.json())


def delete_data(data):
    headers = {'Content-type': 'application/json'}
    the_id=data['ownerID']
    #delete_url='http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner/'+the_id +'?access_token=EjtuNKCsu0WDnVMjqHoAlK7EX6wQjbDHNfWvgqtF6spYOpWrEWhYW860bvqzEcVS'
    delete_url = 'http://ec2-13-229-129-125.ap-southeast-1.compute.amazonaws.com:3000/api/owner/923199-95-8770?access_token=EjtuNKCsu0WDnVMjqHoAlK7EX6wQjbDHNfWvgqtF6spYOpWrEWhYW860bvqzEcVS'
    response = requests.delete(delete_url, headers=headers)

the_real_list = read_data()
convert_to_json(the_real_list)