from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges


def confirm_release(conn, user, data):
    get(conn,demolitions,data.origin,lock=True)
    return update(conn,demolitions,data.origin,allowed=data.allowed)
