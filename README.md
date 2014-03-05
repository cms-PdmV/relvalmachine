# RelValMachine

CMS PdmV RelValMachine service

### Dependencies

To install all required dependencies for RelValMachine use [pip](https://pypi.python.org/pypi/pip) - a tool for installing and managing Python packages. Use this command to install all dependencies:

    pip install -r requirements.txt


### Database configuration

To configure database at first you should set correct `ENVIRONMENT` in `relval/config.py` file.
If you run relval machine locally then just edit `relval/configuration/local.properties` file with correct connection parameters.
If you want to deploy on virtual machine check `deployment-descriptor.md` file for detail instructions.

After that You can create database with following command:

    python relval/database/create.py

If You want to drop database for whatever reason you can use fallowing command:

    python relval/database/drop.py

### Deployment

If you want to deploy application into production/development server look at
`deployment-descriptor.md` file for detail instruction how to prepare virtual
machine and deploy application.

To run RelValMachine use this command:

    python run.py

### Unit tests

You can run unit tests using command:

    python tests_run.py

All unit tests are located in `tests` package
