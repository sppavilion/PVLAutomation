In-case one wishes to run the automation from his/her laptop or any automation host please follow simple steps to install required modules:

1. SCP the 'bat' folder (from:/acadia_qa/automation/R1.3.1/) to destination server
2. sudo apt-get install python-pip
3. sudo pip install robotframework
4. sudo pip install pexpect
5. sudo pip install xmltodict
6. sudo pip install requests
7. sudo apt-get install libssl-dev
8. sudo pip install paramiko 




Steps to execute automation:

1.Upgrade chassis
2.Upgrade host(initiator)
3.Make sure both have same kernel version
4.SCP the 'bat' folder (from:/acadia_qa/automation/R1.3.1/) to destination server.
5.change variables.py and setup.conf according to your setup

	***In setup.conf you mainly need to check:

	mgmt_ip=172.25.26.10
	mgmt_user=admin
	mgmt_pass=admin
	mgmt_ssh_user=root
	mgmt_ssh_pass=2bon2b
	initiator_ip=172.25.26.200
	initiator_user=root
	initiator_pass=2bon2b

	----choose path for logs according to your suit(sanity/snapshot/pq_sanity)---------
	logs_upload_server_http_fld_base_path=/var/www/html/a_logs/pq_sanity/
	#logs_upload_server_http_fld_base_path=/var/www/html/a_logs/sanity/
	#logs_upload_server_http_fld_base_path=/var/www/html/a_logs/snapshot/

	***In variables.py
	zone = "1"
	assign_ctrl_port_ip = "192.168.2.89"(Note:single IP(single path) or multiple comma seperated IP(multi-path))
	controller_node = "node4"(Note:single node(single path) or multiple comma seperated nodes(multi-path))
	recipient_email="sagar.neve@paviliondata.com,abhaya.vagare@paviliondata.com"

6.make sure you have assigned the ip to controller and is accessible from initiator,there are no media groups already present for same zone.
7.Do CD into bat/testsuites/PDS_Automation/
	Execute automation using:

	nohup ./run_automation.sh -l debug -s <suite-name> &
	Currently supported suite-names are: Sanity.robot, Snapshot-Sanity.robot, PQ-Sanity.robot
	
	----for Sanity-------
	nohup ./run_automation.sh -l debug -s Sanity.robot

	----for PQ-Sanity----
	nohup ./run_automation.sh -l debug -s PQ-Sanity.robot

	----for Snapshot-Sanity----
	nohup ./run_automation.sh -l debug -s Snapshot-Sanity.robot

8.logs files are stored in
	bat/logs/

9.you can check the logs of on going automation tests in debug_logs.txt file unders logs directory.

/acadia_qa/automation/R1.3.1/bat/logs$ tail -f debug_logs.txt

	

10.In case you want to mail the same logs to different recipients you can seprately excute SendMail suit
 after updating "recipient_email" in varibles.py using following command

pybot SendMail.robot from bat/testsuites/PDS_Automation/ 
