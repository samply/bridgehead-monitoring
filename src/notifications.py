import json, logging
from vars import ZABBIX_API_TOKEN, BRIDGEHEAD_ADMIN
from report_to_beam_proxy import reportToBeamProxy
from create_action import check_existing_action
   
def create_user(users_to_create):
    
    params = []
    for user in users_to_create:
        params.append({
            "username": user.split("@")[0],
            "passwd": "22a154a327eae04708ccf3e35854a3c97ff09d751",
            "roleid": "5",
            "usrgrps": [
            {
                "usrgrpid": "7"
            }
            ],
            "medias": [
                {
                    "mediatypeid": "1",
                    "sendto": [
                    user
                            ],
                    "active": 1,
                    "severity": 56,
                    "period": "1-7,00:00-24:00"
            }
            ]
        })
    
    data = json.dumps({
        "url" : "ZABBIX_API_URL",
        "payload" : {
        "jsonrpc": "2.0",
        "method": "user.create",
        "params": params,
        "id": 1,
        "auth": ZABBIX_API_TOKEN
        },
        })
    
    response = reportToBeamProxy(data, metadata="Create User for - " + str(users_to_create))
    
    if response is None:
        logging.critical("User could not be created")
        return
    json_data = response.json()[0]

    json_body = json.loads(json_data["body"])
    
        # Check if the item was successfully created
    if "result" in json_body:
        user_list = ", ".join(users_to_create)
        logging.info("User: " + user_list + " created as Guest")
        return json_body['result']['userids']
    else:
        logging.error(f"Fehler beim Erstellen des Users - {json_body}")
        return None
    
    
    
def check_user():
        
    #username = BRIDGEHEAD_ADMIN.split('@')[0]
    
    data = json.dumps({
        "url" : "ZABBIX_API_URL",
        "payload" : {
        
            "jsonrpc": "2.0",
            "method": "user.get",
            "params": {
                "output": ["username"]
            },
            "auth": ZABBIX_API_TOKEN,
            "id": 1
            }
        })

    response = reportToBeamProxy(data, metadata="Check Bridgehead Admins")
    
    if response is None:
        logging.critical("Next attempt in x seconds")
        check_user()    

    json_data = response.json()[0]
    json_body = json.loads(json_data["body"])

    usernames = {item["username"]: item["userid"] for item in json_body["result"]} 

    userids = []
    users_to_create = []
    for user in BRIDGEHEAD_ADMIN.split(","):
        split_user = user.split("@")[0].strip()
        if split_user not in usernames.keys():
            users_to_create.append(user.strip())
        else:
            logging.info("User " + user.strip() + " already exist")
            userids.append(usernames[split_user])
    
    if users_to_create:
        res = create_user(users_to_create)
        if isinstance(res, list):
            userids.extend(res)
    
    check_existing_action(userids)
                
