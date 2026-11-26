from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import demolitions_service as service
from domain.demolitions_model import demolitions
from domain.demolitions_schemas import ConfirmRelease

router = APIRouter()

@router.get('/demolitions')
def list_demolitions(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, demolitions)


@router.post('/demolitions/confirm-release')
def confirm_release(data: ConfirmRelease, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.confirm_release(conn, user, data)
        record(conn, user, 'demolitions.confirm_release')
        return output
