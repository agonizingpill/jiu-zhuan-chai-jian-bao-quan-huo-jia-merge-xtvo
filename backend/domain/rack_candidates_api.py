from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import rack_candidates_service as service
from domain.rack_candidates_model import rack_candidates
from domain.rack_candidates_schemas import SuggestPair, RecordCandidate

router = APIRouter()

@router.get('/rack_candidates')
def list_rack_candidates(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, rack_candidates)


@router.post('/rack_candidates/suggest-pair')
def suggest_pair(data: SuggestPair, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.suggest_pair(conn, user, data)
        record(conn, user, 'rack_candidates.suggest_pair')
        return output


@router.post('/rack_candidates/record-candidate')
def record_candidate(data: RecordCandidate, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.record_candidate(conn, user, data)
        record(conn, user, 'rack_candidates.record_candidate')
        return output
