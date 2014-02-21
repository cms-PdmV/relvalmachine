# RelValMachine

## CMS PdmV RelValMachine service

### Dependencies

To install all required dependencies for RelValMachine use [pip](https://pypi.python.org/pypi/pip) - a tool for installing and managing Python packages. Use this command to install all dependencies:

    pip install -r requirements.txt


### Database configuration

To configure database at first you should edit relval/config.py file.
`SQLALCHEMY_DATABASE_URI` property must be set to correct database url.
After that You can create database with following command:

    python relval/database/create.py

If You want to drop database for whatever reason you can use fallowing command:

    python relval/database/drop.py

### Deployment

Use this command if you want to deploy RelValMachine:

    python run.py

### Unit tests

You can run unit tests using command:

    python tests_run.py

All unit tests are located in `tests` package
