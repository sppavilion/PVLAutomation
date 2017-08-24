To run nvmeof scalability test-cases,
1) To run Volume scalability (50 vol, FIO)
```screen -dmSL {jobname} pybot -L DEBUG -i Volume-Scalability --argumentfile .test-data/ubuntu_16.10_params.txt --exitonfailure --skipteardownonexit NVMEoF_Scalability.robot```
 
OR
2) To run FS partition read-write test, 
```screen -dmSL {jobname} pybot -L DEBUG -i FS-Partitions-Scalability --argumentfile centos_7.3_params.txt --exitonfailure --skipteardownonexit NVMEoF_Scalability.robot```

OR
3) To run Snapshot read test,
```screen -dmSL {jobname} pybot -L DEBUG -i Volume-FS-Snapshot-MNT --argumentfile centos_7.3_params.txt --exitonfailure --skipteardownonexit NVMEoF_Scalability.robot```

To run complete test which include all above tests,
```screen -dmSL {jobname} pybot -L DEBUG --argumentfile centos_7.3_params.txt --exitonfailure --skipteardownonexit NVMEoF_Scalability.robot```

Content of .test-data/ubuntu_16.10_params.txt
`
--variable os_distro:"ubuntu"
--variable os_version:"16.10"
--variable kernel_version:""
-s UBUNTU 16.10
-N UBUNTU 16.10
--debugfile UBUNTU_16.10_debug.log
`
