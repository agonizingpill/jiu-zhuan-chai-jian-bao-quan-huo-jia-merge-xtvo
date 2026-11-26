from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges
from domain.yard_service import drop_stack, invalidate_by_reading


def survey_stack(conn, user, data):
    src=get(conn,demolitions,data.origin)
    need(src['allowed'],'来源地不在保全范围')
    need(100<=data.length<=500 and 0<=data.perforation<=1 and (data.wet is None or 0<=data.wet<=70)
         and 1<=data.pieces<=250,'砖垛实测输入不合法')
    return insert(conn,brick_stacks,**data.model_dump(),initial_wet=data.wet,
                  weighed=False,merged=False,reading_rev=0)


def confirm_moisture(conn, user, data):
    row=get(conn,brick_stacks,data.stack,lock=True)
    need(not row['merged'] and 0<=data.wet<=70,'该砖垛已归档或实测越界')
    output=update(conn,brick_stacks,data.stack,wet=data.wet,weighed=True,
                  reading_rev=row['reading_rev']+1)
    drop_stack(conn,data.stack)
    if row['weighed']:
        invalidate_by_reading(conn,user,data.stack)
    return output
