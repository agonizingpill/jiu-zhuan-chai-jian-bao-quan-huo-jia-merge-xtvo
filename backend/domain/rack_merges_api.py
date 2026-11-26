from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import rack_merges_service as service
from domain.rack_merges_model import rack_merges
from domain.rack_merges_schemas import PackRack

router = APIRouter()

@router.get('/rack_merges')
def list_rack_merges(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, rack_merges)


@router.post('/rack_merges/pack-rack')
def pack_rack(data: PackRack, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.pack_rack(conn, user, data)
        record(conn, user, 'rack_merges.pack_rack')
        return output
