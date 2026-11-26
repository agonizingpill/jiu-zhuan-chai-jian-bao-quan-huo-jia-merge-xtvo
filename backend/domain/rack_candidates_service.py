from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges


def suggest_pair(conn, user, data):
    target=get(conn,brick_stacks,data.stack)
    standard=get(conn,demolitions,target['origin'])['load_grade']
    sources={r['code'] for r in scan(conn,demolitions) if r['load_grade']==standard and r['allowed']}
    pool=[r for r in scan(conn,brick_stacks) if r['origin'] in sources and r['code']!=target['code']
          and r['weighed'] and not r['merged']]
    need(target['weighed'] and not target['merged'] and len(pool)>=6,'至少需要六个相同用途的复测垛')
    return submit(user,{'target':target,'samples':pool})


def record_candidate(conn, user, data):
    run=result(user,data.token); stats=run['result']
    return insert(conn,rack_candidates,code=data.code,member=run['input']['target']['code'],
      pair=stats['pair'],cluster_size=stats['size'],token=data.token)
