from google.cloud import recommender_v1
from google.cloud import secretmanager_v1beta1 as secretmanager
from atlassian import Jira
from pprint import pprint

def get_secret(project_id, secret, version):
    client = secretmanager.SecretManagerServiceClient()
    secret_version_path = f'projects/{project_id}/secrets/{secret}/versions/{version}'
    response = client.access_secret_version(name=secret_version_path)
    return response.payload.data.decode('utf-8')

def detect_projects_with_excess_permissions(project_id):
    client = recommender_v1.RecommenderClient()

    parent_string = 'projects/{project}/locations/{location}/recommenders/{recommenders}'.format(
            project=project_id,
            location='global',
            recommenders='google.iam.policy.Recommender'
        )
    response = client.list_recommendations(parent=parent_string)
    for recommendation in response:

        print("=" * 100)
        print(recommendation.name)
        print(recommendation.associated_insights[0].insight)
        print(recommendation)
        print("=" * 100)
        create_jira_ticket(recommendation.name, recommendation.associated_insights[0].insight, recommendation)

    if not response:
        print("No recommendations found.")

def create_jira_ticket(name, insight, recommendation):
    project_id = "1075187666000"
    secret_name = "prd-jira-automation"
    secret_version = "latest"

    JIRA_USER = "infrasec-automation"
    PRD_JIRA_SERVER = "https://jira.unity3d.com"
    PRD_JIRA_SECRET_NAME = "prd-jira-automation"
    PRD_JIRA_PASSWORD = get_secret(project_id, secret_name, secret_version)
    prd_jira = Jira(
        url=PRD_JIRA_SERVER,
        username=JIRA_USER,
        password=PRD_JIRA_PASSWORD)
    print(prd_jira)

    summary = f"Unused Projects | {name} | Cost Savings Potential"
    template = f"""<insert template data>
Insight: {insight}
Recommendation: {recommendation}"""

    new_task = prd_jira.create_issue(
        fields={
            'project': {'key': 'SECURITY'},
            'issuetype': {
                "name": "Finding"
            },
            'summary': summary,
            'description': template,
            "labels": ["UnusedProjects", "2021-Solutions", "GCP"],
            "components": [{"name": "GCP Hardening"}],
            "customfield_10505": {"id": "37417"},  # department
            "customfield_13716": {"id": "12707"},  # security-team
            "customfield_16402": {"id": "16400"}  # Best Practices
        }
    )
    issue = new_task['key']
    print(issue)
    prd_jira.add_attachment(issue, f"/{name}")

if __name__ == "__main__":
    project_id = ""  # Enter your project ID
    detect_projects_with_excess_permissions(project_id)
