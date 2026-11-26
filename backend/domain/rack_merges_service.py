from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges


def pack_rack(conn, user, data):
    candidate=get(conn,rack_candidates,data.candidate)
    keys=sorted([candidate['member'],candidate['pair']])
    left,right=[get(conn,brick_stacks,key,lock=True) for key in keys]
    source=[get(conn,demolitions,x['origin']) for x in (left,right)]
    need(source[0]['load_grade']==source[1]['load_grade'] and all(x['allowed'] for x in source),
         '两垛用途不相同或来源未放行')
    need(not left['merged'] and not right['merged'],'一个砖垛已有货架')
    need(all(x['weighed'] and x['wet']<=6 for x in (left,right)),'新近返潮的砖垛禁止合架')
    pack=insert(conn,rack_merges,**data.model_dump(),pieces=left['pieces']+right['pieces'])
    for key in keys: update(conn,brick_stacks,key,merged=True)
    return pack
