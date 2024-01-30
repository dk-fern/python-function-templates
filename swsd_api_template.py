import requests
import os

#####################################################################
# Function was used in a termination audit in which specific        #
# Solar Winds Service Desk tickets titled "Termination: <user>"     #
# needed to be pulled and a ticket number returned.                 #
#####################################################################

def swsd_incident(first_name :str, last_name :str) -> str: #DONE

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
