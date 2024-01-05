# function_templates
Repo to hold templates for commonly used functions in scripts. Taken/sanatized from script that pulled data from multiple API endpoints, filtered data based on delta/full database sync needs, wrote that data to a SQL database, alerted and logged errors.

# Current Functions Include:
## Func1_apiPull_pagation_sql_emailAlerts_logging.py:
- Pull data from API, filter data based on day of month (useful for scheduled tasks and differentiating delta/full backups)
- Pull data from API with pagation loop
- Write to SQL database, first validates and updates rows based on any criteria needed
- Send alert email
- Write to local appLog
- Convert datetime to a format valid for SQL

## log_function.py
- Uses logging library to write more detailed log to error.log file
