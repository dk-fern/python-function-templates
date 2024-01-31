# function_templates
Repo to hold templates for commonly used functions in scripts. Taken/sanatized from script that pulled data from multiple API endpoints, filtered data based on delta/full database sync needs, wrote that data to a SQL database, alerted and logged errors.

# Current Functions Include:
## Microsoft_graphAPI_template
- Includes two functions used for interacting with microsoft graph apis
- The first function is used to authenticate and return an authentication token with a custom application created in Microsoft Entra
- The second function uses that token to pull user data from Microsoft Entra. Currently it pulls a users job title

## log_function_template:
- General function to create and write to an error log when errors occur

## python_sql_template:
- Connect and write to a sql database
- Will write an update query first, then add new rows based on any criteria given

## restfulApiPull_pagation_emailAlerts_logging_template:
- Created from a script that pulled from two different restful API endpoints
- The first function pulls a list of IDs from one endpoint and writes them to, and returns a list
- The second function uses that list to pull data from a second endpoint and pulls more granular data

## swsd_api_template:
- Used in a script to pull data from Solar Winds Service Desk restful API

## log_function.py
- Uses logging library to write more detailed log to error.log file
