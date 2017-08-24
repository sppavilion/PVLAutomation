#------------------------------------------------common variables for sanity and nvme_compatibility---
media_group_name = "MEDIA_GRP"
zone = "2"
#recipient_email = "sagar.neve@paviliondata.com,abhaya.vagare@paviliondata.com"
recipient_email="list.india.all@paviliondata.com,list.sw@paviliondata.com"
assign_ctrl_port_ip = "192.168.10.14"
#----------------------------------------------------variables used for sanity tests
controller_node = "node14"
volume1="av1"
volume2="av2"
volume3="av3"
snapshot_name= "snap1"
snapshot_name2="snap2"
clone_name = "clone"
fs_type="ext4"
#----------------------------------------------------nvme_compatibility_variables-------------
stress_connect_disconnect_cnt = 10
stress_volume_flavor = "INSANE"
vol_size = 100
default_reservation = 100
fio_sorce = "/resources/fio"
nvme_mdts_enabled = 1
stress_volumes_cnt = 8
#nvme_compatibility_matrix={'ubuntu':['16.10','16.04','15.10','15.04','14.10','14.04.5','14.04'],'centos':['6.8','7.1','7.2','7.0','7.3'],'sles':['12','12-sp1','12-sp2']}
nvme_compatibility_matrix={'ubuntu':['16.10'],'centos':['6.8']}
nvme_host_driver_branch = "R1.3.1"
nvme_host_driver_version = "5600"
mp_device_disconnect_order="primary-secondary"
#mp_device_disconnect_order="secondary-primary"
#------------------------------------------------------NVME scalability------------------------
single_controller_ip = "192.168.1.101"
volume_scalability_stress_volume_count=45
fs_partition_scalability_volume_count=2
fs_partition_scalability_volume_size=2048
fs_partition_scalability_no_of_partitions=2
#------------------------------------------------------other tests variables-------------------
volume_name = "Volume"
longevity_stress_loop_count = "5"
default_vol_size = 100
stress_media_grp_cnt = 5
stress_volume_size = 100
stress_volume_reservation = 100
stress_clone_reservation = 100
stress_max_snapshots_per_vol = 10
stress_max_clones_per_snapshot = 10
stress_allowed_max_assignd_vol = 10
stress_allowed_max_assignd_snap = 10
stress_allowed_max_assignd_clone = 10
stress_con_discon_vol_cnt = 3
