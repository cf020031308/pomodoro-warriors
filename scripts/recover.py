'''
Occasionally the majority of data in the files completed.data and
pending.data would be purged.
Maybe it is because of the use of cloud storage I don't know.
Using taskserver or simply git to manage the data is recommended.
And here comes a script to recovery completed.data and pending.data
from backlog.data.
'''

import os
import json
import time
import datetime
from collections import OrderedDict


def utc2time(date):
    return int(
        time.mktime(
            datetime.datetime.strptime(date, '%Y%m%dT%H%M%SZ').timetuple()) -
        time.timezone)


def recover(input_folder, output_folder=None):
    assert os.path.isdir(input_folder)
    if output_folder:
        assert os.path.isdir(output_folder)
    else:
        output_folder = input_folder
    tasks = OrderedDict()
    with open(os.path.join(input_folder, 'backlog.data')) as f:
        for line in f.readlines():
            task = json.loads(line)
            for k in task:
                try:
                    task[k] = utc2time(task[k])
                except:
                    pass
            if task.get('tracked') and task['tracked'][0] == 'P':
                del task['tracked']
            if task.get('tags'):
                task['tags'] = ','.join(task['tags'])
            if task.get('annotations'):
                for anno in task.pop('annotations'):
                    task['annotation_%s' % utc2time(anno['entry'])] = anno[
                        'description']
            for k in task:
                task[k] = json.dumps(
                    task[k] if isinstance(task[k], basestring)
                    else str(task[k]),
                    ensure_ascii=False)
            tasks[task['uuid']] = task

    for path in ('completed.data', 'pending.data'):
        with open(os.path.join(input_folder, path)) as f:
            for line in f.read().decode('utf8').splitlines():
                row = line.split('" ')
                row[0] = row[0][1:]
                row[-1] = row[-1][:-2]
                task = dict((col + '"').split(':', 1) for col in row)
                tasks[task['uuid']] = task

    pending, completed = [], []
    for task in tasks.values():
        _task = '[%s]' % ' '.join(
            sorted(['%s:%s' % kv for kv in task.items()])).encode('utf8')
        if task['status'] in ('"pending"', '"waiting"'):
            pending.append((task['entry'], _task))
        else:
            completed.append((task['entry'], _task))
    pending = [x[1] for x in sorted(pending, key=lambda x: x[0])]
    completed = [x[1] for x in sorted(completed, key=lambda x: x[0])]

    with open(os.path.join(output_folder, 'completed.data'), 'w') as f:
        f.write('\n'.join(completed))
    with open(os.path.join(output_folder, 'pending.data'), 'w') as f:
        f.write('\n'.join(pending))


if __name__ == '__main__':
    recover(
        os.path.join(os.getenv('HOME'), '.task'),
        os.path.dirname(os.path.realpath(__file__)))
