import requests
import json
import pyodbc
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
import os
from typing import List
import traceback

#############################################################################################
# This template was taken from a script that pulled from two APIs.                          #
# - The first API pull wrote IDs to a list                                                  #
# - The second API pull used the list to pull more granular detail from a                   #
#   second API endpoint                                                                     #
# Functions included:                                                                       #
# - Pull from api, store api data to a list                                                 #
# - Pull from api                                                                           #
# - Write to appLog                                                                         #
# - Send email                                                                              #
# - Convert datetime                                                                        #
#                                                                                           #
# Comment out all statements to print to console in production                              #
##############################################################################################


#--Global Variables used throughout script--#
token = "<Your API Key>"

script_name = "<Your script name>"

#--Pull information from an API and write to an empty list. Designed to run as a schedule task to run a full backup monthly and delta backups more frequently--# 
def api_pull_to_list() -> List[str]:
    import requests
    from typing import List
    import traceback


    return_list = []

    url = "<Your API endpoint URL>"
    global token, script_name
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    
    #--Use current date to run full backup at the first of the month--#
    today = datetime.now()
    cur_day = today.day
    ###################################################################

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # formatted_data = json.dumps(data, indent=4)
            for item in data:
                if cur_day == 1:
                    return_list.append(item["<Item to append to list>"])
                else:
                    #Insert the parameter you wish to filter by for smaller daily backups. E.g. item["training_status"] == "Active"
                    if item["<Filter parameter>"] == "<Filter value>":
                        return_list.append(item["<Item to append to list>"])

            return return_list
        
        else:
            print(f'Error: {response.status_code}')
            write_to_appLog(f'Error: {response.status_code}')
            return None

    except Exception as e:
        function_name = 'api_pull_to_list'
        error_title = f'Exception in {script_name}: {function_name}'
        error_msg = f'Exception in {function_name}: {str(e)}\n{traceback.format_exc()}'
        
        write_to_appLog(error_msg)
        send_email(error_title, error_msg)
        print(f'Error: {str(e)}')

#--Pull data from an api with a pagation loop. Then use a write_to_sql function to write data to a database--#
def api_pull_with_pagation(input_variable :str) -> None:
    import requests

    url = "<Your API endpoint URL>"
    global token, script_name
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    #--Following couple of lines used for pagation loop--#
    current_page = 1
    continue_processing = True
    while continue_processing:
        params = {
            'input_variable': input_variable,
            'page': current_page,
            'per_page': 500,
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                #Break from pagation loop if no data is returned
                if not data:
                    continue_processing = False

                #--Script wrote info to a sql databse, but from this point, anything can be done with the data--#

                for item in data:
                    #Use replace method to sanatize input in order to avoid sql injection
                    var1 = str(item['var1']).replace("'", "''")
                    var2 = str(item['var2']).replace("'", "''")
                    var3 = str(item['var3']).replace("'", "''")
                    var4 = str(item['var4']).replace("'", "''")
                    var_date = convert_datetime(item['var_date']) #convert_datetime function will return string if applicable and will sanatize single quotes to accout for value errors
                    if not enrollment_date:
                        enrollment_date = ''

                    # Use a sql query function to write each row
                    write_to_sql(var1, var2, var3, var4, var_date)

                #Increase page count for pagation loop
                current_page += 1

            else:
                print(f'Error: {response.status_code}')
                write_to_appLog(f'Error: {response.status_code}')
                return None

        except Exception as e:
            function_name = 'api_pull_with_pagation'
            error_title = f'Exception in {script_name}: {function_name}'
            error_msg = f'Exception in {function_name}: {str(e)}'
            
            write_to_appLog(error_msg)
            send_email(error_title, error_msg)
            print(f'Error: {str(e)}')



#--Write error to appLog. Ensures that the appLog file is in the same directory as the script--#
def write_to_appLog(error_msg :str) -> None:
    cwd = os.getcwd()
    try:
        curDate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
        with open(f'{cwd}\\appLog.txt', 'a') as f:
            f.write(f'\n{curDate} - {error_msg}')
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

#--Function to send emails for when errors take place, takes email subject and body message--#
def send_email(error_title :str, error_msg :str):
    smtpBody = error_msg
    smtpSubject = error_title
    smtpServer = 'smtp.office365.com'
    smtpPort = 587
    smtpUser = '<sender email address>'
    smtpRecipient = '<recipient address>'
    smtpSecret = '<sender password>' #--Use -> os.environ['env variable name']

    curDate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")

    try:
        ms = smtplib.SMTP(smtpServer, smtpPort)
        ms.ehlo()
        ms.starttls()
        ms.login(smtpUser, smtpSecret)
        msg = EmailMessage()
        msg.set_content(f'{curDate} - {smtpBody}')
        msg['Subject'] = smtpSubject
        msg['From'] = smtpUser
        msg['To'] = smtpRecipient
        ms.send_message(msg)
        ms.quit()
    except Exception as e:
        function_name = 'send_email()'
        error_msg = f'Exception in {function_name}: {str(e)}'
        write_to_appLog(error_msg)

        #print(f'Error: {str(e)}')

#--Convert api datetime to a yyyy-mm-dd hh:mm:ss format. Return None if conversion is not applicatble--#
def convert_datetime(old_datetime :str) -> str:
    if type(old_datetime) == str:
        try:
            #Update parsed_datetime to your current datetime format. Currently is taking format that looks like this: "2023-01-06T19:00:04.000Z"
            parsed_datetime = datetime.strptime(old_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
            formatted_datetime_string = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            #Uses replace method to avoid sql injection
            return str(formatted_datetime_string).replace("'", "''")
        except Exception as e:
            #print(f'Error: {str(e)}')
            return None
    else:
        return None
