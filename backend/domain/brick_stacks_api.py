from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import brick_stacks_service as service
from domain.brick_stacks_model import brick_stacks
from domain.brick_stacks_schemas import SurveyStack, ConfirmMoisture

router = APIRouter()

@router.get('/brick_stacks')
def list_brick_stacks(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, brick_stacks)


@router.post('/brick_stacks/survey-stack')
def survey_stack(data: SurveyStack, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.survey_stack(conn, user, data)
        record(conn, user, 'brick_stacks.survey_stack')
        return output


@router.post('/brick_stacks/confirm-moisture')
def confirm_moisture(data: ConfirmMoisture, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.confirm_moisture(conn, user, data)
        record(conn, user, 'brick_stacks.confirm_moisture')
        return output
