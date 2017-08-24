TO run connect-all testsuite on single vm execute below command -

```screen -dmSL {jobname} pybot -L DEBUG --argumentfile centos_7.3_params.txt --exitonfailure --skipteardownonexit NVMEoF_connect-all_Suite.robot```

Content of `centos_7.3_params.txt`
`
--variable os_distro:"centos"
--variable os_version:"7.3"
--variable kernel_version:""
-s CENTOS 7.3
-N CENTOS 7.3
--debugfile CENTOS_7.3_debug.log
`