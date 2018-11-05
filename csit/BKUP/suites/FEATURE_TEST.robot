*** Settings ***
Documentation     A test suite with tests for SDWAN LAN conenctivity.
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
Suite Setup         STARTUP
Suite Teardown      CLEANUP
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ../Topology/devices.py
Variables         ../Variables/SANITY/Variables.py
Library           Collections
Library           String
Library           ../libraries/VersaCommands.py  C1  ${CURDIR}/../Topology/Devices.csv    WITH NAME   C1
Library           ../libraries/VersaCommands.py  C2  ${CURDIR}/../Topology/Devices.csv    WITH NAME   C2
Library           ../libraries/Commands.py
Resource          ../libraries/Resource.robot

*** Test Cases ***
Create Post staging template


*** Keywords ***
STARTUP
    C1.login
    C2.login


CLEANUP
    C1.close
    C2.close