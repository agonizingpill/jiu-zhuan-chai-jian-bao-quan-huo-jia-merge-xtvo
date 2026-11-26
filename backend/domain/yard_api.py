from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from domain import yard_service as service

router = APIRouter()

@router.get('/yard')
def yard_board(user=Depends(actor)):
    with transaction() as conn:
        return service.board(conn, user)


@router.post('/yard/assess')
def assess_yard(user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.assess(conn, user)
        record(conn, user, 'yard.assess')
        return output
