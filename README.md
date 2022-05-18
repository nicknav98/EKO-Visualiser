# NERC Scripts, Personal Repo

## User warnings, potential points of improvement

Visualise script uses psycopg to connect to postgres, pandas produces warning:

Tag(development, 1.0)

UserWarning: pandas only support SQLAlchemy connectable(engine/connection) ordatabase string URI or sqlite3 DBAPI2 connectionother DBAPI2 objects are not tested, please consider using SQLAlchemy
  warnings.warn(