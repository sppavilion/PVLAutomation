import inspect
import subprocess
import logging
import os
import json
import requests
from resources.__init__ import API_DICT
import time
import ast
import lib.Constants as constants

format = "%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d %(message)s"
logging.basicConfig(level=logging.DEBUG, format=format)
logger = logging.getLogger(__file__)
task_dict = dict()
cookies = [0, 0]

def run(cmd, hostname, password):
    cmd_str = '/usr/bin/sshpass -p %s ssh root@%s '%(password, hostname)
    cmd_str += ' -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    cmd_str += ' \" %s \" '%(cmd)
    result = None
    try:
        result = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result.wait()
        return result.returncode, str(result.stdout.readlines())
    except Exception as E:
        return 1,str(E)

def get_properties(filename):
    file_exists = 1
    filePath = ""
    path = os.getcwdu()
    projectDir = path.strip().split("/" + constants.project_name)[0]
    projectDir = projectDir + "/" + str(constants.project_name)
    for root, subFolders, files in os.walk(projectDir):
        if filename in files:
            filePath = root + "/" + filename
            file_exists = 1

    if file_exists == 0 and filePath and filePath != "":
        logger.debug ("Properties/Config file "+str(filename)+" is not present in the project directory.")
        return None

    properties = dict()
    if os.path.exists(filePath):
        with open(filePath, "r") as properties_file:
            for line in properties_file:
                if line[:1] != '#':
                    (k,v) = line.split("=")
                    k = k.strip()
                    v = v.strip()
                    properties[k]=v.rstrip().replace('"','')
            properties_file.close()
        return properties
    else:
       print (filePath + " is not present ..")
       return None


def get_object_id(object_type, object_name):
    logger.debug("In " + inspect.stack()[0][3])
    properties = get_properties("setup.conf")
    get_object_id_api = ( API_DICT[inspect.stack()[0][3]]) % (properties['mgmt_ip'], properties['mgmt_ip'], object_type, object_name )
    logger.debug ("Executing API - "+str(get_object_id_api))
    (resp, code) = call_api(get_object_id_api, properties)
    logger.debug("API response:" + str(resp))
    logger.debug("API response code:" + str(code))
    if "taskid" in resp:
        status = check_task_status(resp["taskid"])
        if (status != "Completed"):
            check_task_status(resp["taskid"])
    else:
        status = code
    return resp["id"]


def check_task_status(taskid):
    logger.debug("In " + inspect.stack()[0][3])
    properties = get_properties("setup.conf")
    count = 180
    while 1:
        tresp = get_task(taskid)
        task_dict[taskid] = tresp
        if (tresp["state"] == 1 or tresp["state"] == 3):
            logger.info("Current task state: " + str(tresp["displayState"]))
            time.sleep(float(properties["wait_time"]))
            count -= 1
            if (count == 0):
                logger.info("Time out(" + properties['wait_time'] + ") reached. Exiting. Current task state: " + str(
                    tresp['displayState']))
                return tresp["displayState"]
        if (tresp["state"] == 0 or tresp["state"] == 2):
            logger.info("Final task state: " + str(tresp["displayState"]))
            return tresp["displayState"]

    
def get_task(task_id):
    logger.debug("In " + inspect.stack()[0][3])
    properties = get_properties("setup.conf")
    get_task_api = ( API_DICT[inspect.stack()[0][3]] ) % ( properties['mgmt_ip'], properties['mgmt_ip'], task_id )
    logger.debug("Executing API - " + str(get_task_api))
    (resp, code) = call_api(get_task_api, properties)
    logger.debug("API response:" + str(resp))
    logger.debug("API response code:" + str(code))
    return resp

def call_api(api_json, properties, server_type="mgmt"):
    """ This actually executes the api and returns the response a JSON response"""
    global cookies
    logger.debug("In " + inspect.stack()[0][3])
    if type(api_json) != dict:
        logger.debug("Received api is not in dictionary format.")
        api_json = ast.literal_eval(api_json)

    header = {"Content-Type": api_json["header"]["Content-Type"], "XSRF-TOKEN": cookies[1],
              "X-XSRF-TOKEN": cookies[1], "Referer": "https://" + api_json["ip"] + "/swagger-ui.html"}
    logger.debug("Header:" + str(header))
    logger.debug("Method:" + str(api_json["method"]))
    logger.debug("API url:" + str(api_json["api_url"]))
    logger.debug("Requested Data:" + str(api_json["req_data"]))

    r = requests.request(api_json["method"], api_json["api_url"], headers=header, data=json.dumps(api_json["req_data"]),
                         cookies={"JSESSIONID": str(cookies[0])}, verify=False)
    if (r.status_code != 200):
        logger.debug("Admin log in")
        cookies = admin_login(api_json, properties, server_type)
        return call_api(api_json, properties, server_type)

    if (r.text != ""):
        r_json = json.loads(r.text)
        return r_json, str(r.status_code)
    else:
        return None, str(r.status_code)

def admin_login(api_json, properties, server_type):
    """This log-in to system and creates the cookies - which are used to pass in different API callings"""
    if (server_type == "mgmt"):
        ip = properties["mgmt_ip"]
        user = properties["mgmt_user"]
        password = properties["mgmt_pass"]
    elif (server_type == "chs"):
        ip = properties["chs_ip"]
        user = properties["chs_user"]
        password = properties["chs_pass"]
    else:
        logger.error("Server type is not supported")
    s = requests.session()
    r = s.post("https://" + ip + "/api/v1.0/auth/login?password=" + password + "&username=" + user,
               {"Accept": "application/json"}, verify=False)
    if (r.status_code != 200):
        logger.debug("LOG IN FAILED")
    jid = r.cookies["JSESSIONID"]
    xrf = r.cookies["XSRF-TOKEN"]
    logger.debug("JSESSIONID:" + jid)
    logger.debug("COOKIES:" + xrf)
    return jid, xrf


def list_all_vols_copies():
    logger.debug("In " + inspect.stack()[0][3])
    properties = get_properties("setup.conf")
    list_all_vols_copies_api = (API_DICT[inspect.stack()[0][3]]) % ( properties['mgmt_ip'], properties['mgmt_ip'] )
    logger.debug("Get all volumes/copies api - : " + str(list_all_vols_copies_api))
    (resp, code) = call_api(list_all_vols_copies_api, properties)
    logger.debug("API response:" + str(resp))
    logger.debug("API response code:" + str(code))
    return resp, code


def get_key_value(status_code, resp, key1, value1, key2):
    if ((status_code == "200") and type(resp) is list) and len(resp) != 0:
        for iter in range(0, len(resp)):
            resp_dict = resp[iter]
            for k, v in resp_dict.items():
                if k == key1 and v == value1:
                    return resp_dict[key2]
        return "None"
    else:
        return "None"


