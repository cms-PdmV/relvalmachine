# RelVal Machine

### Database configuration

To configure database at first you should edit relval/config.py file.
`SQLALCHEMY_DATABASE_URI` property must be set to correct database url.
After that You can create database with following command:

    python relval/database/create.py

If You want to drop database for whatever reason you can use fallowing command:

    python relval/database/drop.py
