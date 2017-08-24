# NVMEoF Compatibility Automation
NVMEoF Compatibility Automation focuses on testing the access and basic connectivity of pavilion's storage array (here after referred as target) from clients having different OS distributions of different OS versions ( here after refferred as host or initiator).
This involves installing some software's on the host/initiator like nvme-cli, OFED driver, host-driver etc, which is taken care by automation. However, there are prerequisites that this automation expects to be fulfilled.

### Prerequisites - setup
A machine/server having libvirt and components related virtualization already installed So that user can create virtual machines on it.
The machine/server having mellanox interfaces - which can be added to the virtual machines.
Virtual machine's base template for the OS distribution and version under consideration. The template should have following packages pre-installed:
  - Build Essentials
  - Default kernel header / devel / source
  - OFED Driver (If kernel version is lesser than 3.15 , not applicable for uek kernel)
There is a target box which has at-least 4 volumes exposed - so that any host can connect to them.

### Current setup in use
Greenidge (172.25.26.207) is a server which has libvirt and all related components of virtualization installed.
Greenidge has the base templates of the different OS distributions versions too.
Greenidge has 63 mellanox virtual functions to be used by virtual machines.

### How to execute automation
Considering the current setup in use - Greenidge  below are the brief instructions on executing the automation.
1. Copy the automation code to a directory on Greenidge
```
$ scp -r /acadia_qa/automation/R1.3.1/bat/ root@172.25.26.207:/
```
2. Login to the Greenidge and cd into `bat` directory.
```sh
$ ssh root@172.25.26.207
$ cd /acadia_qa/automation/R1.3.1/bat/
```
3. Update the parameters based on the test-setup `config/setup.conf`
   ```
    $ vi /acadia_qa/automation/R1.3.1/bat/config/setup.conf
    mgmt_ip={target_management_ip}
    mgmt_ssh_user={user}
    mgmt_ssh_pass={password}
    ...
    nvmeOf_nvme_cli_path={nvme-cli_source_dir}
    custom_driver_user={username}
    custom_driver_host={ip_adress}
    custom_driver_pass={password}
    custom_driver_location={absolute_host_driver_tar_file_path}
    ```

4. Update the user parameters `resources/variables.py`
    ```
    $ vi /acadia_qa/automation/R1.3.1/bat/resources/variables.py
    media_group_name = {name_of_media_group}
    zone = {zone_number}
    assign_ctrl_port_ip={target_controller_port_ip}
    recipient_email={email_adresses,group_name}
    vol_size = {volume_size_in_GB}
    default_reservation = {percentage(1-100)}
    stress_volume_flavor = {volume_flavor(HIGH,INSANE..)}
    stress_volumes_cnt={integer_value}
    stress_connect_disconnect_cnt={integer_number}
    is_simulation_setup={0|1}
    nvme_compatibility_matrix={'os-distibution':['os-version']}
    nvme_host_driver_branch = {host_driver_branch}
    nvme_host_driver_version = {host_driver_version}
    fio_sorce = {absolute_path_of_fio_source_on_local_system}
    mp_device_disconnect_order={secondary-primary|primary-secondary}
    nvme_mdts_enabled = {0|1}
    ```
    
    Please note following OS distribution and versions are available on Greenidge:
     centos  : 6.8, 7.0, 7.1, 7.2, 7.3
     rhel    : 7.0, 7.1, 7.2, 7.3
     ubuntu  : 14.04, 14.04.5, 14.10, 15.04, 15.10, 16.04, 16.10
     sles    : 11-sp4, 12, 12-sp1, 12-sp2
     oel     : 6.8, 7.0, 7.1, 7.2
    
    Please provide os-distribution : [os-version] dictionary properly.
    Example :
    ```
    nvme_compatibility_matrix={'ubuntu':['16.10'],'centos':['7.1','7.2'], 'sles':['11-sp4','12'], 'rhel':['7.0'], oel:['6.8']}
    ```   
    Note: If you want to compile host-driver with custom change, set `nvme_host_driver_version` to random one, and provide details in setup file.
    
    

5. cd into `testsuites/PDS_Automation` directory and start nvmeOf compatibility automation by executing following command:
To run whole testsuit, use below command
 Common steps -
 - Specify `nvme_host_driver_branch` & `nvme_host_driver_version` in variables files which is exactly same as target.
 - Delete running VM's.
 ````
 i)   Non MP Compatibility test
      - Create media-group manually and specify name of media-group into parameters file `media_group_name`
      - Assign IP to single active controller port IP manually.
      - Specify single assignment controller port IP i.e `assign_ctrl_port_ip="192.168.2.102""`
      - execute below command to start test
        `python start_pnvmEf_automation.py -i Complete`
        
 ii)  Connet-Disconnect Stress test(MP/Non MP)
      - Create media-group manually and specify name of media-group into parameters file `media_group_name`
      - Assign IP to single active controller port IP manually.
      - Specify stress count `stress_connect_disconnect_cnt`
      - Specify single assignment controller port IP i.e `assign_ctrl_port_ip="192.168.2.102""`
        `python start_pnvmEf_automation.py -i Stress`
      
 iii) MP Compatibility Test
      - Create media-group manually and specify name of media-group into parameters file `media_group_name`
      - Assign IP to multiple active controller port IP manually.
      - Specify single assignment controller port IP i.e `assign_ctrl_port_ip="192.168.2.102,192.168.1.101""`
      - execute below command to start test
        `python start_pnvmEf_automation.py -i Complete`
      
 iv)   Host Driver build test
      - execute below command to start test
      `python start_pnvmEf_automation.py -i Host-Driver`
      
 v)  Host initialization test
      - execute below command to start test
      `python start_pnvmEf_automation.py -i BASE`
      
 vi) Only FIO test
      - execute below command to start test
      `python start_pnvmEf_automation.py -i FIO`

IMP - to start automation in background, Use `screen` command,
`screen -dmSL job_name python start_pnvmEf_automation.py -i <tag>`
To check log of jobs,
`screen -x job_name`

This command will start automation, and after execution of testsuits, email will be sent to provided recipients. Email contains total testsuit report, summary file, detailed log file.
````
6. To check automation log of any OS distribution,
    `tailf .test-data/pabot_results/{process_num}/pnvmEf\ compliance\ Stress/{OS_Distro}_debug.log`
 Example -
    `tailf .test-data/pabot_results/1/pnvmEf\ compliance\ Stress/CENTOS_6.8_debug.log`


### Send report to all pavilion team
To Send an email to all pavilion team, Change the email addresses of below parameters to "list.india.all@paviliondata.com,list.sw@paviliondata.com"
`recipient_email="list.india.all@paviliondata.com,list.sw@paviliondata.com"`

To change the subject like 'compatibility OR Compatibility (MP device) OR MP connect-disconnect OR connect-disconnect'
Find out the variable called `test_name` in parser.py file & update the value .

For example,
Tester want's to send an email for MP connect-disconnect automation,
Update parser file,
`test_name = "MP Connect-Disconnect"`

Executes the send mail python class.
`python send_pnvmEf_automation_mail.py`


### Test Case coverage by this automation
Following is the list and sequence of test-cases that are executed through this automation to validate if the host os distrubution and version is compatible with Pavilion's Target.

Setup : Precheck for base template virtual machine, nvme-cli.
Teardown : Delete cloned vm

  - Create clone from base template virtual machine
  - Assign available virtual function/ Mellanox interface to clonned virttual machine. 
    Start the cloned VM and assign static IP to mellanox interfaces in VM
  - Download and compile provided host-driver version
  - Copy and compile nvme-cli
  - Create & assign volumes
  - Discover target volumes
  - Connect to 4 volumes
  - Configure FIO & Run FIO (Sequential Write/Read BS=128k,512k,1M)
  - Create file-system(XFS/EXT4), mount and perform IO on mounted location and unmount
  - Disconnect all volumes one by one
  - Multiple times connect-disconnect volumes.
  - Unassign & delete volumes.
