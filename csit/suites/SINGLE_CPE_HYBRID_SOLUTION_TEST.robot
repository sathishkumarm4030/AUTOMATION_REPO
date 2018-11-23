*** Settings ***
Documentation     A test suite with tests for SDWAN HYBRID Solution.
...               Topology:-
...               ____________________________
...               | VersaDirector |
...               |___________________________|
...               |
...               |
...               |
...               _____________|_______________
...               | WanCtrller1 |
...               |____________________________|
...               | |
...               | |
...               | |
...               INTERNET/MPLS
...               | |
...               | |___
...               ______|__ ___|___
...               | | | |
...               LAN1--+ CPE1 | | CPE2 +--LAN1
...               |________| |_______|
...
...
...               Testplan Goals:-
...               1. CHECK IF IP ADDRESS IS SET AND INTERFACE IS UP.
Suite Setup       STARTUP
Suite Teardown    CLEANUP
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../Topology/devices.py
Variables         ../libraries/Variables.py
Library           Collections
Library           String
Library           ../libraries/VersaLib.py    C1_MUM    ${CURDIR}/../Topology/Devices.csv    WITH NAME    CPE1
Library           ../libraries/VersaLib.py    C2_MUM    ${CURDIR}/../Topology/Devices.csv    WITH NAME    CPE2
Library           ../libraries/LinuxLib.py    VM1_MUM    ${CURDIR}/../Topology/Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    VM2_MUM    ${CURDIR}/../Topology/Devices.csv    WITH NAME    VM2

*** Variables ***
${Topo_file}      ${CURDIR}/../Topology/Devices.csv
${j2_templates_path}    ${CURDIR}/../libraries/J2_temps
${PST}            Post_staging_template.j2
${est}  Established

*** Test Cases ***
Testcase: SDWAN to SDWAN connectivity check both links
    ${result}=    CPE1.get interface status  intf_name=${cpe1['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE1.get interface status  intf_name=${cpe1['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status  intf_name=${cpe2['ptvi_intf_wc1']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE2.get interface status  intf_name=${cpe2['ptvi_intf_wc2']}
    CHECK RESULT    actual=${result}    expected=up
    ${result}=    CPE1.get bgp nbr status       nbr_ip=${cpe1['WC1_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}
    ${result}=    CPE1.get bgp nbr status       nbr_ip=${cpe1['WC2_ESP_IP']}
    CHECK RESULT    actual=${result}    expected=${est}

Testcase: Ping Test VM1 To VM2(1 LAN)
    Ping Test VM1 To VM2(1 LAN)
Testcase: Ping Test VM2 To VM1(1 LAN)
    Ping Test VM2 To VM1(1 LAN)
Testcase: Ping Test VM1 To VM2(10 LANS)
    Ping Test VM1 To VM2(10 LANS)
Testcase: Ping Test VM2 To VM1(10 LANS)
    Ping Test VM2 To VM1(10 LANS)
Testcase: Iperf3 Test VM1 To VM2
    Iperf3 Test VM1 To VM2


*** Keywords ***
STARTUP
    [Documentation]    Make connecection to Versa devices
    #    CPE1.create_PS_and_DG    Post_staging_template.j2    Device_group_template.j2    PS_main_template_modify.j2
    #    CPE1.pre_onboard_work    Device_template.j2    Staging_server_config.j2    staging_cpe.j2
    #    CPE1.cpe_onboard_call
    #    ${CPE1_dev_info_on_vd} =    CPE1.get_device_info
    #    log to console    ${CPE1_dev_info_on_vd}
    #    CPE2.pre_onboard_work    Device_template.j2    Staging_server_config.j2    staging_cpe.j2
    #    CPE2.cpe_onboard_call
    #    ${CPE2_dev_info_on_vd} =    CPE2.get_device_info
    #    log to console    ${CPE2_dev_info_on_vd}
    #    ${a} =    get variables
    #    log to console    ${a}
        CPE1.cross login
        CPE2.cross_login
        VM1.VM_pre_op
        VM2.VM_pre_op
        ${cpe1}    CPE1.get_data_dict
        set suite variable    ${cpe1}
        #log to console    ${cpe1}
        ${cpe2}    CPE2.get_data_dict
        set suite variable    ${cpe2}
        #log to console    ${cpe2}
        ${vm1}    VM1.get_data_dict
        set suite variable    ${vm1}
#        log to console    ${vm1}
        ${vm2}    VM2.get_data_dict
        set suite variable    ${vm2}
#        log to console    ${vm2}

CLEANUP
    log to console    "sasasa"

CHECK RESULT
    [Arguments]    ${actual}    ${expected}=True
    [Documentation]    Check result contains expected value
    log to console    ${actual}
    log to console    ${expected}
    Run Keyword And Continue On Failure    should contain    ${actual}    ${expected}


Ping Test VM1 to VM2(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${vm2['lan'][1]['second_host']}
    ${result}=    VM1.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM1 to VM2(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    11
    \    ${destip}=    set variable    ${vm2['lan'][${vlan}]['second_host']}
    \    log to console    ${destip}
    \    ${result}=    VM1.Shell Ping    ${destip}
    \    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(1 LAN)
    [Tags]    HYBRID
    ${destip}=    set variable    ${vm1['lan'][1]['second_host']}
    ${result}=    VM2.Shell Ping    ${destip}
    CHECK RESULT    actual=${result}

Ping Test VM2 to VM1(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    1    11
    \    ${destip}=    set variable    ${vm1['lan'][${vlan}]['second_host']}
    \    log to console    ${destip}
    \    ${result}=    VM1.Shell Ping    ${destip}
    \    CHECK RESULT    actual=${result}

Iperf3 test VM1 to VM2
    [Tags]    HYBRID
    ${destip}=    set variable    ${vm2['lan'][1]['second_host']}
    VM2.send_commands_and_expect    pkill iperf3 &
    sleep    10s
    VM2.send_commands_and_expect    iperf3 -s &
    ${result}=    VM1.send_commands_and_expect    iperf3 -c ${destip}
    Should Contain    ${result}    iperf Done.