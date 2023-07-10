# Zenki-X
### Least Privilege automation for GCP 

Zenki-X is a Python script that helps identify Google Cloud projects with excess permissions and automatically creates Jira tickets to notify the project owners. The script uses the Google Cloud Recommender API to fetch recommendations for excess permissions and the Atlassian Jira API to create Jira tickets. Because of the use of the Google Recommender API this script outputs low to no impact.

The script performs the following steps:

* Connects to the Google Cloud Recommender API and fetches recommendations for excess permissions in Google Cloud projects.

* For each recommendation, extracts the necessary information such as project ID, recommendation ID, and URL.

* Generates a Jira ticket with the extracted information, including a summary and description.

* Creates the Jira ticket and prints the Jira issue key.


## Prerequisites:
Before using the script, ensure that you have the following prerequisites in place:

* Python: The script requires Python to be installed on your system. You can download Python from the official website: https://www.python.org/downloads/

* Google Cloud Project: This project requires a GCP project that you’ll place into the script to create jira tickets.

* Google Cloud SDK: Install the Google Cloud SDK, which provides the necessary command-line tools for interacting with Google Cloud services. You can download the SDK from the official website: https://cloud.google.com/sdk/docs/install

* Atlassian Jira: Ensure that you have access to an Atlassian Jira instance and valid credentials (server URL, username, and password) to create Jira tickets. These credentials are automatically grabbed for you, just ensure you have the atlassian python package installed.

* Python Packages: Install the required Python packages by running the following command:
```
pip install google-cloud-recommender google-cloud-secret-manager google-api-python-client google-auth atlassian-python-api
```
## Usage:
To use the script, follow these steps:

* Ensure that you have met all the prerequisites mentioned in the "Prerequisites" section.

* Clone the repo

* Open a terminal or command prompt and navigate to the directory where the script file is located.

* Run the script using the following command:

```
python Zenki.py
```

* You might be asked to authtenicate yourself to the GCP org when running this script if you are please authorize the authenication process. 


The script will connect to the Google Cloud Recommender API, fetch the recommendations for excess permissions, generate Jira tickets, and print the Jira issue key for each ticket created. Review the ticket by taking the issue key and searching for it in Jira. 

Notes: You can edit the labels section and replace “4110-Security” with your own team allowing for you to search and create dashboards easier. No changes are required to run this code, but this might be something useful to change. 

You can use the discussion page on the repo or reach out directly to jonathan.gibson@unity3d.com for questions about this script. 
