from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges


def survey_stack(conn, user, data):
    src=get(conn,demolitions,data.origin)
    need(src['allowed'],'来源地不在保全范围')
    need(100<=data.length<=500 and 0<=data.perforation<=1 and 0<=data.wet<=70 and 1<=data.pieces<=250,
         '砖垛实测输入不合法')
    return insert(conn,brick_stacks,**data.model_dump(),weighed=False,merged=False)


def confirm_moisture(conn, user, data):
    row=get(conn,brick_stacks,data.stack,lock=True)
    need(not row['merged'] and 0<=data.wet<=70,'该砖垛已归档或实测越界')
    return update(conn,brick_stacks,data.stack,wet=data.wet,weighed=True)
