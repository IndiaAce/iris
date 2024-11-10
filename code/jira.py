import requests
import json
import sqlite3

JIRA_BASE_URL = "https://your_jira_instance.atlassian.net"
JIRA_PROJECT_KEY = "TI"
JIRA_AUTH = ("your_email@example.com", "your_api_token")
JIRA_HEADERS = {
    "Content-Type": "application/json"
}

# Function to create a Jira ticket based on PIR details
def create_jira_ticket(pir_id):
    connection = sqlite3.connect('intelligence.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PIRs WHERE id = ?", (pir_id,))
    pir = cursor.fetchone()
    connection.close()

    if not pir:
        print(f"No PIR found with ID {pir_id}.")
        return

    description, priority, date_added, status, intelligence_gaps = pir[1:]
    jira_payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"PIR: {description}",
            "description": f"Priority: {priority}\nDate Added: {date_added}\nStatus: {status}\nIntelligence Gaps: {intelligence_gaps}",
            "issuetype": {
                "name": "Task"
            },
            "priority": {
                "name": priority
            }
        }
    }

    response = requests.post(f"{JIRA_BASE_URL}/rest/api/2/issue", 
                             data=json.dumps(jira_payload), 
                             auth=JIRA_AUTH, 
                             headers=JIRA_HEADERS)
    
    if response.status_code == 201:
        print(f"Successfully created Jira ticket for PIR ID {pir_id}.")
    else:
        print(f"Failed to create Jira ticket for PIR ID {pir_id}. Status Code: {response.status_code}, Response: {response.text}")

# Function to update Jira ticket status when PIR status changes
def update_jira_ticket(pir_id):
    connection = sqlite3.connect('intelligence.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PIRs WHERE id = ?", (pir_id,))
    pir = cursor.fetchone()
    connection.close()

    if not pir:
        print(f"No PIR found with ID {pir_id}.")
        return

    description, priority, date_added, status, intelligence_gaps = pir[1:]
    
    # Find the Jira ticket using the summary field
    search_payload = {
        "jql": f"summary ~ \"PIR: {description}\"",
        "fields": ["id"]
    }

    search_response = requests.post(f"{JIRA_BASE_URL}/rest/api/2/search", 
                                    data=json.dumps(search_payload), 
                                    auth=JIRA_AUTH, 
                                    headers=JIRA_HEADERS)

    if search_response.status_code != 200:
        print(f"Failed to find Jira ticket for PIR ID {pir_id}. Status Code: {search_response.status_code}, Response: {search_response.text}")
        return

    issues = search_response.json().get('issues', [])
    if not issues:
        print(f"No Jira ticket found for PIR ID {pir_id}.")
        return

    issue_id = issues[0]['id']
    update_payload = {
        "fields": {
            "status": {
                "name": status
            }
        }
    }

    update_response = requests.put(f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_id}", 
                                   data=json.dumps(update_payload), 
                                   auth=JIRA_AUTH, 
                                   headers=JIRA_HEADERS)

    if update_response.status_code == 204:
        print(f"Successfully updated Jira ticket for PIR ID {pir_id}.")
    else:
        print(f"Failed to update Jira ticket for PIR ID {pir_id}. Status Code: {update_response.status_code}, Response: {update_response.text}")

if __name__ == "__main__":
    # Example usage
    create_jira_ticket(1)
    update_jira_ticket(1)
