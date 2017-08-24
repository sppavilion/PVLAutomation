import lib.API.Snapshot_utils as snapshot_utils

for i in range(1,5):
    snapname = 'snap'+str(i)
    print ("Creating snapshot "+str(snapname))
    resp, status = snapshot_utils.create_snapshot(snapname,"test")
    print ("Create Snapshot TC output -- > Response:"+str(resp)+" status:"+str(status))
    assert (status == 'Completed'), "Failed to create snapshot "+str(snapname)
    print ("deleting snapshot "+str(snapname))
    resp, status = snapshot_utils.del_snapshot(snapname)
    print ("Delete snapshot TC output -- > Response:"+str(resp)+" status:"+str(status))
    assert (status == 'Completed'), "Failed to delete snapshot " + str(
        snapname)





