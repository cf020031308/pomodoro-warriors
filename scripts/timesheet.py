import json
import datetime

import requests

from settings import TIMESHEET_ACCOUNT, TIMESHEET_HOST


class Proxy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        def func(url, params=None, **kwargs):
            return self.func(
                'http://%s%s' % (owner.HOST, url),
                params,
                headers=dict(
                    kwargs.pop('headers', {}),
                    Authorization='Bearer %s' % instance.token),
                **kwargs)
        return func


class TimeSheet(object):
    HOST = TIMESHEET_HOST
    _TOKEN = None

    GET = Proxy(requests.get)
    POST = Proxy(requests.post)

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
        return self.GET('/project').json()

    def put(self, date, projectId, hours, content):
        data = {
            'date': date.strftime('%Y-%m-%d'),
            'hours': hours,
            'content': content,
            'hasSold': 0}
        if projectId:
            data['projectId'] = projectId
        else:
            data.update(
                projectId='self_define_project_id',
                projectName='etc')
        if 'y' != raw_input(
                '%s\nconfirm?[y]' %
                json.dumps(
                    data, indent=2, sort_keys=True, ensure_ascii=False)):
            return
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
