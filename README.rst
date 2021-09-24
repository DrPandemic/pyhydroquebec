#############
PyHydroQuebec
#############


TODO
####

* Add automated tests

Installation
############

::

    pip install pyhydroquebec


Usage
#####

Print your current data

::

    pyhydroquebec -u MYACCOUNT -p MYPASSWORD


List your current contracts

::

    config.yaml PYHQ_OUTPUT=MQTT registry.gitlab.com/ttblt-hass/pyhydroquebec:master
        pyhydroquebec -u MYACCOUNT -p MYPASSWORD -l


Print help

::

    usage: pyhydroquebec [-h] [-u USERNAME] [-p PASSWORD] [-j] [-i] [-c CONTRACT]
                        [-l] [-H] [-t TIMEOUT] [-V] [--detailled-energy]
                        [--start-date START_DATE] [--end-date END_DATE]

    optional arguments:
        -h, --help                          show this help message and exit
        -u USERNAME, --username USERNAME    Hydro Quebec username
        -p PASSWORD, --password PASSWORD    Password
        -j, --json                          Json output
        -i, --influxdb                      InfluxDb output
        -c CONTRACT, --contract CONTRACT    Contract number
        -l, --list-contracts                List all your contracts
        -H, --hourly                        Show yesterday hourly consumption
        -t TIMEOUT, --timeout TIMEOUT       Request timeout
        -V, --version                       Show version

    Detailled-energy raw download option:
        --detailled-energy                  Get raw json output download
        --start-date START_DATE             Start date for detailled-output
        --end-date END_DATE                 End date for detailled-output


MQTT DAEMON
###########

::

   cp config.yaml.sample config.yaml

Note: If 'frequency' is not set the "daemon" will collect the data only one time and stop

Edit config.yaml

::

    MQTT_USERNAME=mqtt_username MQTT_PASSWORD=mqtt_password MQTT_HOST=mqtt_ip MQTT_PORT=mqtt_port CONFIG=config.yaml mqtt_pyhydroquebec


With Docker

::

    MQTT_USERNAME=mqtt_username MQTT_PASSWORD=mqtt_password MQTT_HOST=mqtt_ip MQTT_PORT=mqtt_port CONFIG=config.yaml PYHQ_OUTPUT=MQTT registry.gitlab.com/ttblt-hass/pyhydroquebec:master


Prometheus Server
#################

::

   PYHQ_USER=email PYHQ_PASSWORD=password PYHQ_CONTRACT=contract_number prometheus_pyhydroquebec

With Docker

::

    docker run -e PYHQ_USER=email -e PYHQ_PASSWORD=password -e PYHQ_CONTRACT=contract_number -e PYHQ_OUTPUT=PROMETHEUS registry.gitlab.com/ttblt-hass/pyhydroquebec:master

More information `about the Prometheus integration can be found here <./prometeus.rst>`_.

Docker
######

Docker image list: https://gitlab.com/ttblt-hass/pyhydroquebec/container_registry

::

    docker run -e PYHQ_USER=*** -e PYHQ_PASSWORD=*** registry.gitlab.com/ttblt-hass/pyhydroquebec:master

Docker variables
"""""""""

    **PYHQ_USER** - Required
        `-e PYHQ_USER=myusername`

    **PYHQ_PASSWORD** - Required
        `-e PYHQ_PASSWORD=mypassword`

    **PYHQ_OUTPUT**

    - `-e PYHQ_OUTPUT=TEXT` - Default
    - `-e PYHQ_OUTPUT=JSON`
    - `-e PYHQ_OUTPUT=INFLUXDB`
    - `-e PYHQ_OUTPUT=PROMETHEUS`
    - `-e PYHQ_OUTPUT=CONTRACT`

    **PYHQ_CONTRACT**

        `-e PYHQ_CONTRACT=332211223`

Build multiarch docker images
##############################

::

    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    docker buildx create --use
    docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64 -f Dockerfile-multiarch .


Dev env
#######

::

    make env


Run test
########

::

    USERNAME=myhydrousername PASSWORD=myhydropassword tox
