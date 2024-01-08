
#--Global script name for logging/emails
script_name = '<Your script name>'

def graph_api_authentication() -> str: #DONE
    import msal
    import os
    
    global script_name
    
    try:
        #--Application (client) ID in configured Azure Application
        CLIENT_ID = os.environ['client_id']
        #--Azure tenant ID
        TENANT_ID = os.environ['tenant_id']
        #--Thumbprint found after uploading cert in "App registrations" > "<Your Application>" > "Certificates & Secrets"
        THUMBPRINT = os.environ['thumbprint']
        AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'  

        #---use openssl to generate key/cert pair. Upload cert to Azure and receive cert thumbprint. This is then linked to the private key---#
        #######################################################################################################################################
        # COMMAND TO GENERATE PRIVATE KEY: openssl genrsa -out <key_name_with_date>.key 2048                                                  #
        # COMMAND TO GENERATE PUBLIC CERT: openssl req -new -key <key_name_previously_generated> -out <cer_name_match_key_name>.cer -days 182 #
        #######################################################################################################################################
        
        CERT = {'thumbprint': THUMBPRINT,
                'private_key': open(r'<Path to your .key file>').read()
                }
        
        # Begin authentication with Graph api
        app = msal.ConfidentialClientApplication(
            client_id=CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CERT
            )

        SCOPE = ["https://graph.microsoft.com/.default"]
        # Determine if authentication was successful
        result = app.acquire_token_silent(SCOPE, account=None)

        if not result:
            result = app.acquire_token_for_client(scopes=SCOPE)
        # --------------ACCESS TOKEN -----------------#
        if "access_token" in result:
            access_token = result["access_token"]
        #---------------------------------------------#

        else:
            print(result.get("error"))
            print(result.get("error_description"))

    except Exception as e:
        print(f"Error: {str(e)}")
        function_name = 'graph_api_authentication'
        error_title = f'Exception in {script_name}: {function_name}'
        error_msg = f'Exception in {function_name}: {str(e)}'
        
        #--Insert functions that will write to an application log and send an email if error occurs
        write_to_appLog(error_msg)
        send_email(error_title, error_msg)

    return access_token

#--azure_lookup currently looks up the job title of the user passed in--#
def azure_lookup(access_token :str, user :str) -> str: #DONE
    import requests
    
    global script_name
    
    try:
        # Define endpoint, headers variables
        graph_endpoint = "https://graph.microsoft.com/v1.0/users"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        # create search parameters within AAD
        filter_query = f"displayName eq '{user}'" #DisplayName can be changed depending on which parameter you want to search by. Check docs here: (https://github.com/AzureAD/microsoft-authentication-library-for-python)
        request_url = f"{graph_endpoint}?$filter={filter_query}"

        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            if len(user_data['value']) > 0:
                # --Target user's job title. If jobTitle == None, the account is disabled--
                info = user_data['value'][0]['jobTitle']
                return(info)
            else:
                return("404 Error: User not found")

        else:
            return(f"Failed to retrieve user:{response.text}")

    except Exception as e:
        print(f"Error: {str(e)}")
        function_name = 'graph_api_authentication'
        error_title = f'Exception in {script_name}: {function_name}'
        error_msg = f'Exception in {function_name}: {str(e)}'
        
        #--Insert functions that will write to an application log and send an email if error occurs
        write_to_appLog(error_msg)
        send_email(error_title, error_msg)

#--swsd_incident currently looks up info from swsd api filtering by items with "Termination" in the title, looks for user's first and last name and returns the ticket number--#
def swsd_incident(first_name :str, last_name :str) -> str: #DONE
    import requests
    import os
    token = os.environ['swsd_token']

    url = f'https://api.samanage.com/incidents?title=*Termination*'
    headers = {
    'X-Samanage-Authorization': f'Bearer {token}',
    'Accept': 'application/json',
    }
    # list of incidents with termination in the name
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        response = response.json()
        for data in response:
            ticket_name = data['name']
            if "Employee Termination" in ticket_name:
                if first_name in ticket_name:
                    if last_name in ticket_name:
                        return data['number']
                    else:
                        return "Needs Verification"
                else:
                    pass
