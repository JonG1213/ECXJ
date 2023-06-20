from google.cloud import recommender_v1
from atlassian import Jira
from google.cloud import secretmanager_v1beta1 as secretmanager
from google.protobuf.json_format import MessageToDict

def detect_projects_with_excess_permissions(project_name):
    client = recommender_v1.RecommenderClient()

    parent_string = 'projects/{project}/locations/{location}/recommenders/{recommenders}'.format(
        project=project_name,
        location='global',
        recommenders='google.iam.policy.Recommender'
    )

    response = client.list_recommendations(parent=parent_string)
    for recommendation in response:
        print("=" * 100)
        print(recommendation.name)

        project_id = recommendation.name.split('/')[1]
        insight_id = recommendation.name.split('/')[7]
        url = f"https://console.cloud.google.com/home/recommendations/list/IAM_ROLES?project={project_name}"
        print(project_id, insight_id)
        create_jira_ticket(project_id, url)
        break

def get_secret(project_id, secret, version):
    client = secretmanager.SecretManagerServiceClient()
    secret_version_path = f'projects/{project_id}/secrets/{secret}/versions/{version}'
    response = client.access_secret_version(name=secret_version_path)
    return response.payload.data.decode('utf-8')

def create_jira_ticket(project_id, url):
    secret_name = "prd-jira-automation"
    secret_version = "latest"

    JIRA_USER = "infrasec-automation"
    PRD_JIRA_SERVER = "https://jira.unity3d.com"
    PRD_JIRA_SECRET_NAME = "prd-jira-automation"
    PRD_JIRA_PASSWORD = get_secret(project_id, secret_name, secret_version)
    prd_jira = Jira(
        url=PRD_JIRA_SERVER,
        username=JIRA_USER,
        password=PRD_JIRA_PASSWORD
    )
    summary = f"Excess Permissions | {project_name} | Security hardening"
    description = f"""
    GCP's Native IAM Excess Permissions detection system has detected your project: {project_name} currently has service accounts with excess permissions. Please review and update the permissions accordingly.
    Recommendations:

    If any of these service accounts are not in used, please delete or detach role. If these service accounts were provisioned with Terraform, the permissions will need to be updated there.
    Disclaimer: GCP IAM recommender generates recommendations by comparing a principle a total number of permissions with the permissions that the principal used in the last 90 days. If the role binding was created fewer than 90 days ago, the IAM recommender looks at the principal's permission usage in the time since the binding was created. Before apply any recommendations, please ensure you have the knowledge on how this would affect running services within a project. 

    URL: {url}
    """

    new_task = prd_jira.create_issue(
        fields={
            'project': {'key': 'SECURITY'},
            'issuetype': {"name": "Finding"},
            'summary': summary,
            'description': description,
            "labels": ["ExcessPermissions", "4110-Security", "GCP"],
            "components": [{"name": "GCP Hardening"}],
            "customfield_10505": {"id": "37417"},  # department
            "customfield_13716": {"id": "12707"},  # security-team
            "customfield_16402": {"id": "16400"}  # Best Practices
        }
    )

    issue_key = new_task['key']
    print("Jira ticket created: ", issue_key)

if __name__ == "__main__":
    project_name = "unity-security-playground-test"  # Enter your project ID
    detect_projects_with_excess_permissions(project_name)
