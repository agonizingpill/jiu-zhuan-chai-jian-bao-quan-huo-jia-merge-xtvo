import json
from pathlib import Path
from traceback import print_exc

from core.db import transaction
from core.queueing import QUEUE, broker
from domain.learning import calculate, risk
from domain.yard_service import admit, rescore

pulse = Path('/tmp/compute-heartbeat')

def yard_score(job):
    outcome = risk(job['input'])
    with transaction() as conn:
        summary = admit(conn, job['input'], outcome, token=job['token'])
        if summary is None:
            rescore(conn, job['owner'], job['input'])
    if summary is None:
        return {'status': 'stale', 'detail': '训练读数已更正，该批旧分不回榜'}
    return {'status': 'ready', 'result': {'state': outcome['state'], **summary}}

def serve():
    while True:
        broker.ping()
        pulse.touch()
        item = broker.blmove(QUEUE, f'{QUEUE}:processing', timeout=2, src='LEFT', dest='RIGHT')
        if item is None:
            continue
        job = json.loads(item)
        status = {'owner': job['owner'], 'input': job['input']}
        try:
            if isinstance(job['input'], dict) and job['input'].get('mode') == 'yard_score':
                status.update(yard_score(job))
            else:
                status.update(status='ready', result=calculate(job['input']))
        except ValueError as exc:
            status.update(status='rejected', detail=str(exc))
        except Exception:
            print_exc()
            status.update(status='rejected', detail='计算失败，请检查输入和 worker 日志')
        with broker.pipeline() as pipe:
            pipe.set(f'compute:{job["token"]}', json.dumps(status, allow_nan=False), ex=86400)
            pipe.lrem(f'{QUEUE}:processing', 1, item)
            pipe.execute()
        pulse.touch()

if __name__ == '__main__':
    for raw in broker.lrange(f'{QUEUE}:processing', 0, -1):
        with broker.pipeline() as pipe:
            pipe.lpush(QUEUE, raw)
            pipe.lrem(f'{QUEUE}:processing', 1, raw)
            pipe.execute()
    serve()
