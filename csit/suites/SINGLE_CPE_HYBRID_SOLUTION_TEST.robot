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
Library           ../libraries/VersaLib.py    C1_MUM   ${CURDIR}/../Topology/Devices.csv    WITH NAME    cpe1
Library           ../libraries/VersaLib.py    C2_MUM   ${CURDIR}/../Topology/Devices.csv    WITH NAME    cpe2
Library           ../libraries/LinuxLib.py    VM1_MUM   ${CURDIR}/../Topology/Devices.csv    WITH NAME    VM1
Library           ../libraries/LinuxLib.py    VM2_MUM   ${CURDIR}/../Topology/Devices.csv    WITH NAME    VM2


*** Variables ***
${Topo_file}        ${CURDIR}/../Topology/Devices.csv
${j2_templates_path}    ${CURDIR}/../libraries/J2_temps
${PST}      Post_staging_template.j2

*** Test Cases ***
Ping Test VM1 to VM2(1 LAN)
    [Tags]    HYBRID
    ${destip}=  set variable    ${vm1_data['peer_lan_second_host'][${vm1_data['lan_vlan'][0]}]}
    ${result}=  VM1.Shell Ping    ${destip}
    CHECK RESULT  actual=${result}

Ping Test VM1 to VM2(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    0    10
    \    ${destip}=  set variable    ${vm1_data['peer_lan_second_host'][${vm1_data['lan_vlan'][${vlan}]}]}
    \    log to console  ${destip}
    \    ${result}=  VM1.Shell Ping    ${destip}
    \    CHECK RESULT  actual=${result}



Ping Test VM2 to VM1(1 LAN)
    [Tags]    HYBRID
    ${destip}=  set variable    ${vm2_data['peer_lan_second_host'][${vm2_data['lan_vlan'][0]}]}
    ${result}=  VM2.Shell Ping    ${destip}
    CHECK RESULT  actual=${result}

Ping Test VM2 to VM1(10 LANS)
    [Tags]    HYBRID
    : FOR    ${vlan}    IN RANGE    0    10
    \    ${destip}=  set variable    ${vm2_data['peer_lan_second_host'][${vm2_data['lan_vlan'][${vlan}]}]}
    \    log to console  ${destip}
    \    ${result}=  VM1.Shell Ping    ${destip}
    \    CHECK RESULT  actual=${result}



Iperf3 test VM1 to VM2
    [Tags]    HYBRID
    ${destip}=  set variable    ${vm1_data['peer_lan_second_host'][${vm1_data['lan_vlan'][0]}]}
    VM2.send_commands_and_expect   pkill iperf3 &
    sleep  10s
    VM2.send_commands_and_expect   iperf3 -s &
    ${result}=  VM1.send_commands_and_expect   iperf3 -c ${destip}
    Should Contain  ${result}  iperf Done.


*** Keywords ***
STARTUP
    [Documentation]    Make connecection to Versa devices
#    cpe1.create_PS_and_DG   Post_staging_template.j2  Device_group_template.j2  PS_main_template_modify.j2
#    cpe1.pre_onboard_work   Device_template.j2    Staging_server_config.j2    staging_cpe.j2
#    cpe1.cpe_onboard_call
#    ${cpe1_dev_info_on_vd} =  cpe1.get_device_info
#    log to console  ${cpe1_dev_info_on_vd}
#    cpe2.pre_onboard_work   Device_template.j2    Staging_server_config.j2    staging_cpe.j2
#    cpe2.cpe_onboard_call
#    ${cpe2_dev_info_on_vd} =  cpe2.get_device_info
#    log to console  ${cpe2_dev_info_on_vd}
    VM1.VM_pre_op
    VM2.VM_pre_op
    ${vm1_data}    VM1.get_data_dict
    set suite variable    ${vm1_data}
    ${vm2_data}    VM2.get_data_dict
    set suite variable  ${vm2_data}

CLEANUP
    log to console    "sasasa"

CHECK RESULT
    [Arguments]    ${actual}  ${expected}=True
    [Documentation]    Check result contains expected value
    log to console  ${actual}
    log to console  ${expected}
    Run Keyword And Continue On Failure    should contain  ${actual}    ${expected}