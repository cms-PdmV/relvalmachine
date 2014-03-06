# Deployment descriptor

#### Step by step guide how to deploy relval machine.

## Prerequisites

 - python version 2.6

 - [pip](https://pypi.python.org/pypi/pip) - tool for installing and managing Python packages.

Usually pip is pre-installed software in virtual machines. If it's not installed run command:

    sudo yum install python-pip

 - [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) - tool for creating isolated python environments.
 In order to install virtualenv run command


    pip install virtualenv

## Create virtualenv for RelValMachine

cd into directory where you want to store virtualenv files, then run following commands:

    sudo bash
    virtualenv relvalmachine-virtualenv
    source relvalmachine-virtualenv/bin/activate

Now your virtualenv is activated, you can deactivate it using command: `deactivate`

## Install Oracle drivers

Go into [oracle web page](http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html)
and download following files:

    oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
    oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm
    oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64.rpm

Then run following commands to install downloaded packages:

    sudo bash
    rpm -ivh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
    rpm -ivh oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm
    rpm -ivh oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64.rpm

Configure `oracle-instalntclient`

    echo /usr/lib/oracle/11.2/client64/lib/ > /etc/ld.so.conf.d/oracle.con
    ldconfig
    export ORACLE_HOME=/usr/lib/oracle/11.2/client64
    export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH
    export PATH=$ORACLE_HOME/bin:$PATH

Install `cx_Oracle` library from source. Download [`cx_Oracle` source code](http://cx-oracle.sourceforge.net/) (select Source Code only section)

Extract source code and install `cx_Oracle` with following commands

    sudo bash
    python setup.py build && python setup.py install

## Clone RelValMachine from git

    git clone git@github.com:cms-PdmV/relvalmachine.git

## Install all dependencies

At first make sure that you still using virtualenv created previously, then cd into relvalmachine project directory and run following commands:

    sudo bash
    pip install -r requirements.txt

## Verify configuration

Configuration is stored in file `relval/config.py`.
Before deployment you should set correct `ENVIRONMENT` property
and verify that corresponding configuration file (defined in property `[ENVIRONMENT]_ENV_CONFIG_FILE`)
holds correct database configuration.

After you verify database connection parameters you can create database (if not created yet) with command:

    python relval/database/create.py

## Deploy application

At first make sure that port 80 is open in your virtual machine.
After running command `iptables-save` you should see following line if port 80 is open:

    -A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT

Then you can deploy RelValMachine with command:

    sudo bash
    nohup python run.py &





