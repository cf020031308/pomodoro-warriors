import json
import datetime

import requests

from settings import TIMESHEET_ACCOUNT, TIMESHEET_HOST


class proxy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        def func(url, params=None, **kwargs):
            return self.func(
                'http://%s%s' % (owner.HOST, url),
                params=params,
                headers=dict(
                    kwargs.pop('headers', {}),
                    Authorization='Bearer %s' % instance.token),
                **kwargs)
        return func


class TimeSheet(object):
    HOST = TIMESHEET_HOST
    _TOKEN = None
    _PROJECTS = None

    GET = proxy(requests.get)
    POST = proxy(requests.post)

    @property
    def token(self):
        if not TimeSheet._TOKEN:
            TimeSheet._TOKEN = requests.post(
                'http://%s/auth/login' % self.HOST,
                data=TIMESHEET_ACCOUNT
            ).json()['token']
            assert TimeSheet._TOKEN
        return TimeSheet._TOKEN

    @property
    def projects(self):
        if not TimeSheet._PROJECTS:
            TimeSheet._PROJECTS = {
                project[field]: project
                for project in self.GET('/project').json()
                for field in ('projectId', 'projectName')}
        return TimeSheet._PROJECTS

    def put(self, date, project, hours, content):
        assert not (float(hours) % 0.25), (
            'value of working hours should be times of 0.25')
        data = {
            'project': None,
            'date': date.strftime('%Y-%m-%d'),
            'hours': str(hours),
            'projectId': self.projects.get(
                project, {}).get('projectId', 'self_define_project_id'),
            'projectName': self.projects.get(
                project, {}).get('projectName', project),
            'content': content}
        resp = self.POST('/daily', data=data)
        assert 200 <= resp.status_code < 300, (
            resp.status_code, resp.headers, resp.content)
        return resp

    def get(self, startdate, enddate=None):
        enddate = enddate or startdate
        resp = self.GET(
            '/daily',
            params={
                'startTime': startdate.strftime('%Y-%m-%d'),
                'endTime': enddate.strftime('%Y-%m-%d')})
        for line in resp.content.splitlines():
            line = line.strip()
            if line:
                return json.loads(line)


if __name__ == '__main__':
    ts = TimeSheet()
    print json.dumps(
        ts.get(datetime.date.today() - datetime.timedelta(days=1)),
        indent=2,
        sort_keys=True,
        ensure_ascii=False)
