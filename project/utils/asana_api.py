import asana
from decouple import config

TOKEN = config('ASANA_TOKEN')
WORKSPACE_GID = config('ASANA_WORKSPACE_GID')


class AsanaApiWrapper:
    def __init__(self):
        self.token = TOKEN
        self.workspace_gid = WORKSPACE_GID
        self.client = self._get_client()

    def _get_client(self):
        client = asana.Client.access_token(self.token)
        client.headers = {'asana-enable': 'string_ids'}
        client.options['client_name'] = "test_module"
        return client

    def create_project(self, name):
        return self.client.projects.create_in_workspace(self.workspace_gid, params={'name': name})['gid']

    def update_project(self, gid, name):
        self.client.projects.update(gid, params={'name': name})

    def add_user_to_workspace(self, gid):
        self.client.workspaces.add_user(self.workspace_gid, params={'user': str(gid)})

    def create_task(self, project_gid, user_gid, text):
        return self.client.tasks.create(
            params={'workspace': self.workspace_gid, 'projects': [str(project_gid)],
                    'followers': [str(user_gid)], 'name': text}
        )['gid']

    def update_task(self, task_gid, text, project_gid, user_gid):
        project = list(self.client.tasks.projects(str(task_gid)))[0]['gid']
        follower = self.client.tasks.find_by_id(str(task_gid))['followers'][0]['gid']
        self.client.tasks.update(str(task_gid), params={'workspace': self.workspace_gid, 'name': text})
        self.client.tasks.remove_project(str(task_gid), params={'project': project})
        self.client.tasks.add_project(str(task_gid), params={'project': str(project_gid)})
        self.client.tasks.remove_followers(str(task_gid), params={'followers': [follower]})
        self.client.tasks.add_followers(str(task_gid), params={'followers': [str(user_gid)]})
