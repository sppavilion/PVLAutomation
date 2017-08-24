import inspect
import logging
import lib.Common as common
from resources.__init__ import API_DICT

format = "%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d %(message)s"
logging.basicConfig(level=logging.DEBUG, format=format)
logger = logging.getLogger(__file__)

def create_snapshot(snap_name, vol_name):
    ''' This creates snapshot takes two arguments snapshot name and volume name
    on which the snapshot is to be created. '''
    logger.debug ("In " + inspect.stack()[0][3])
    properties = common.get_properties('setup.conf')
    parent_id = common.get_object_id("Volume", vol_name)
    logger.debug ("volume parent id - "+str(parent_id))
    create_snapshot_api = ( API_DICT[inspect.stack()[0][3]] ) % ( properties['mgmt_ip'], properties['mgmt_ip'], snap_name, "Snapshot", parent_id )
    logger.debug("Create snapshot api - "+str(create_snapshot_api))
    (resp, code) = common.call_api(create_snapshot_api, properties)
    logger.debug("API response code:" + str(code))
    if "taskid" in resp:
        status = common.check_task_status(resp["taskid"])
    else:
        status = code
    return resp, status


def del_snapshot(name):
    ''' This deletes the specified snapshot '''
    logger.debug("In " + inspect.stack()[0][3])
    properties = common.get_properties('setup.conf')
    logger.info("Get the list of snapshots")
    (resp, status) = common.list_all_vols_copies()
    snapshot_id = common.get_key_value(status, resp, "name", name, "id")
    logger.info("The snapshot: " + name + " has id: " + snapshot_id)
    delete_snapshot_api = (API_DICT[inspect.stack()[0][3]]) % (properties['mgmt_ip'], properties['mgmt_ip'], snapshot_id)
    logger.debug("Delete Snapshot API -" + str(delete_snapshot_api))
    (resp, code) = common.call_api(delete_snapshot_api, properties)
    logger.debug("API response:" + str(resp))
    logger.debug("API response code:" + str(code))
    if "taskid_list" in resp:
        status = common.check_task_status(resp["taskid_list"][0])
    else:
        status = code
    return resp, status

