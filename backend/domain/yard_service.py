from datetime import datetime, timezone

from sqlalchemy import select

from core.queueing import submit
from core.records import get, need, scan
from domain.brick_stacks_model import brick_stacks
from domain.yard_model import yard_scores


def _features(row):
    return {'code': row['code'], 'initial': row['initial_wet'],
            'length': row['length'], 'perforation': row['perforation']}


def _view(row):
    return {'code': row['code'], 'origin': row['origin'], 'initial_wet': row['initial_wet'],
            'length': row['length'], 'perforation': row['perforation']}


def _scores(conn):
    query = select(yard_scores).order_by(yard_scores.c.stack)
    return [dict(row) for row in conn.execute(query).mappings()]


def build_payload(conn, targets):
    rows = scan(conn, brick_stacks)
    held = {row['origin'] for row in rows if not row['weighed'] and not row['merged']}
    samples = [row for row in rows
               if row['weighed'] and row['initial_wet'] is not None and row['origin'] not in held]
    return {'mode': 'yard_score',
            'targets': [_features(row) for row in targets],
            'samples': [dict(_features(row), retest=row['wet']) for row in samples],
            'basis': {row['code']: row['reading_rev'] for row in samples}}


def assess(conn, user):
    targets = [row for row in scan(conn, brick_stacks)
               if not row['weighed'] and not row['merged'] and row['initial_wet'] is not None]
    need(targets, '暂无待评分的待复测垛')
    return submit(user, build_payload(conn, targets))


def board(conn, user):
    stacks = {row['code']: row for row in scan(conn, brick_stacks)}
    ranked, unestimable, covered = [], [], set()
    for entry in _scores(conn):
        stack = stacks.get(entry['stack'])
        if stack is None or stack['weighed'] or stack['merged']:
            continue  # 已复测或已合垛的砖垛不在榜
        covered.add(entry['stack'])
        row = _view(stack) | {'score': entry['score'], 'updated': entry['updated']}
        (ranked if entry['score'] is not None else unestimable).append(row)
    ranked.sort(key=lambda row: (-row['score'], row['code']))
    waiting, unscorable = [], []
    for stack in stacks.values():
        if stack['weighed'] or stack['merged'] or stack['code'] in covered:
            continue
        (unscorable if stack['initial_wet'] is None else waiting).append(_view(stack))
    return {'ranked': ranked, 'unestimable': unestimable,
            'waiting': sorted(waiting, key=lambda row: row['code']),
            'unscorable': sorted(unscorable, key=lambda row: row['code'])}


def drop_stack(conn, code):
    conn.execute(yard_scores.delete().where(yard_scores.c.stack == code))


def invalidate_by_reading(conn, user, code):
    affected = [row['stack'] for row in _scores(conn) if code in (row['basis'] or {})]
    if not affected:
        return None
    conn.execute(yard_scores.delete().where(yard_scores.c.stack.in_(affected)))
    targets = [row for row in scan(conn, brick_stacks) if row['code'] in affected
               and not row['weighed'] and not row['merged'] and row['initial_wet'] is not None]
    if not targets:
        return None
    return submit(user, build_payload(conn, targets))


def admit(conn, payload, outcome, token):
    basis = payload.get('basis') or {}
    for code in sorted(basis):
        row = get(conn, brick_stacks, code, lock=True)
        if row['reading_rev'] != basis[code]:
            return None  # 读数已更正，晚到的旧分不回榜
    scores = outcome.get('scores') or {}
    admitted, skipped = [], []
    now = datetime.now(timezone.utc)
    for target in sorted(payload.get('targets') or [], key=lambda item: item['code']):
        row = get(conn, brick_stacks, target['code'], lock=True)
        if row['weighed'] or row['merged'] or row['initial_wet'] is None:
            skipped.append(target['code'])  # 复测入账即撤下，晚来的分数排不进去
            continue
        conn.execute(yard_scores.delete().where(yard_scores.c.stack == target['code']))
        conn.execute(yard_scores.insert().values(stack=target['code'],
                                                 score=scores.get(target['code']),
                                                 basis=basis, token=token, updated=now))
        admitted.append(target['code'])
    return {'admitted': admitted, 'skipped': skipped}


def rescore(conn, owner, payload):
    codes = {item['code'] for item in payload.get('targets') or []}
    targets = [row for row in scan(conn, brick_stacks) if row['code'] in codes
               and not row['weighed'] and not row['merged'] and row['initial_wet'] is not None]
    if not targets:
        return None
    return submit({'sub': owner}, build_payload(conn, targets))
