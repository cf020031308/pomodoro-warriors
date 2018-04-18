# coding: utf8

import datetime

import urllib3
import requests

import utils


urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
KEY = 'jira'


class JIRA(object):
    def __init__(self, host):
        self.host = host
        self.user = host.split('://', 1)[-1].split('@', 1)[0].split(':', 1)[0]
        self.session = requests.Session()

    def jira(self, endpoint, **kwargs):
        kwargs.setdefault('verify', False)
        kwargs.setdefault('allow_redirects', False)
        method, uri = endpoint.split()
        return self.session.request(method.lower(), self.host + uri, **kwargs)

    def Transition(self, task):
        return {
            'id': (
                '21' if 'start' in task
                else '31' if task['status'] == 'completed'
                else '11'
            ),
        }

    def Fields(self, task):
        tags = task.get('tags', [])
        ret = {
            'summary': task['description'],
            'issuetype': {'name': u'缺陷' if 'bug' in tags else u'任务'},
            'assignee': {'name': task.get('@', self.user)},
            'priority': {'name': u'紧急' if 'next' in tags else u'一般'},
            'labels': sorted(
                t for t in tags if t not in ('next', 'ops', 'bug', 'dev')),
        }
        # TODO and timeSpentSeconds
        if 0 and 'estimate' in task:
            ret['timetracking'] = {
                'originalEstimate': '%ss' % int(
                    utils.parse_duration(task['estimate']).total_seconds()),
            }
        if 'due' in task:
            ret['duedate'] = (
                datetime.datetime.strptime(task['due'], '%Y-%m-%dT%H:%M:%S') +
                datetime.timedelta(hours=8)
            ).strftime('%Y-%m-%d')
        return ret

    def Update(self, prior, task):
        ret = {}
        if len(task.get('annotations', [])) > len(
                prior.get('annotations', [])):
            ret['comment'] = [{
                'add': {'body': task['annotations'][-1]['description']}}]
        return ret

    def create_issue(self, task):
        projectKey = task[KEY]
        payload = {
            'fields': dict(self.Fields(task), project={'key': projectKey})}
        resp = self.jira('POST /rest/api/2/issue', json=payload).json()
        key = resp['key']
        task[KEY] = key
        try:
            rapidViewId = self.jira(
                'GET /projects/' + projectKey
            ).headers['Location'].rsplit('rapidView=', 1)[-1].split('&', 1)[0]
            SprintId = self.jira(
                'GET /rest/greenhopper/1.0/xboard/work/allData.json',
                params={
                    'rapidViewId': rapidViewId,
                    'selectedProjectKey': projectKey,
                },
            ).json()['sprintsData']['sprints'][0]['id']
            self.jira(
                'PUT /rest/greenhopper/1.0/sprint/rank',
                json={
                    'idOrKeys': [key],
                    'customFieldId': '10009',
                    'sprintId': SprintId,
                    'addToBacklog': False,
                }
            )
            return '%s created on Jira and added to sprint %s' % (
                key, SprintId)
        except Exception:
            return '%s created on Jira' % key

    def update_issue(self, prior, task):
        key = task[KEY]

        payload = {'fields': self.Fields(task)}
        update = self.Update(prior, task)
        if update:
            payload['update'] = update
        self.jira('PUT /rest/api/2/issue/%s' % key, json=payload)

        pt = self.Transition(prior)
        transition = self.Transition(task)
        if pt['id'] != transition['id']:
            payload['transition'] = transition
            self.jira(
                'POST /rest/api/2/issue/%s/transitions' % key,
                json={'transition': transition})
        return '%s synced to Jira' % key

    def delete_issue(self, key):
        resp = self.jira('DELETE /rest/api/2/issue/%s' % key)
        if resp.status_code < 300:
            return '%s deleted on Jira' % key
        else:
            return 'Failed to delete %s on Jira: %s' % (key, resp.content)


def sync():
    inputs = utils.format_inputs()
    task = inputs.get('task')
    if not task:
        return

    try:
        jira = JIRA(utils.settings.JIRA)
    except Exception:
        return

    prior = inputs.get('prior', {})
    key = task.get(KEY)
    if not key:
        key = prior.get(KEY)
        if key and '-' in key:
            return jira.delete_issue(key)
    elif '-' not in key:
        return jira.create_issue(task)
    elif task['status'] == 'deleted':
        return jira.delete_issue(key)
    elif prior:
        return jira.update_issue(prior, task)
