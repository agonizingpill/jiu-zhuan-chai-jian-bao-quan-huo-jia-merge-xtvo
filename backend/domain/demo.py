from domain.demolitions_model import demolitions
from domain.brick_stacks_model import brick_stacks
from domain.rack_candidates_model import rack_candidates
from domain.rack_merges_model import rack_merges


def stack(code, origin, length, perforation, initial, wet, weighed, pieces):
    return {'code': code, 'origin': origin, 'length': length, 'perforation': perforation,
            'initial_wet': initial, 'wet': wet, 'weighed': weighed, 'pieces': pieces,
            'merged': False, 'reading_rev': 1 if weighed else 0}


_LENGTHS = [193.0, 210.48, 227.96, 194.44, 210.0, 227.48, 193.96, 211.44, 227.0, 193.48, 210.96, 228.44]
_PERFORATIONS = [0.17, 0.28500000000000003, 0.39, 0.17500000000000002, 0.28, 0.395]
_WETS = [3, 4, 5]

LEGACY = [stack(f'BR-{i:02d}', 'DEMO-K' if i % 2 == 0 else 'DEMO-L',
                _LENGTHS[i % 12], _PERFORATIONS[i % 6], _WETS[i % 3] + 0.5, _WETS[i % 3], True, 15 + i)
          for i in range(30)]

# 待复测垛：已登记初测、尚未复测，等待堆场榜出分
PENDING = [
    stack('BR-30', 'DEMO-K', 195.0, 0.18, 3.2, 3.2, False, 24),
    stack('BR-31', 'DEMO-K', 205.0, 0.24, 4.1, 4.1, False, 25),
    stack('BR-32', 'DEMO-K', 215.0, 0.28, 5.0, 5.0, False, 26),
    stack('BR-33', 'DEMO-K', 198.0, 0.20, 6.3, 6.3, False, 27),
    stack('BR-34', 'DEMO-K', 222.0, 0.33, 7.4, 7.4, False, 28),
    stack('BR-35', 'DEMO-K', 190.0, 0.16, 8.6, 8.6, False, 29),
    # 缺初测的垛：不进训练也不出分
    stack('BR-36', 'DEMO-K', 210.0, 0.26, None, None, False, 30),
]

# 训练池：DEMO-M 凭单下已完成复测的垛，覆盖超标与未超标两类样本
POOL = [
    stack('BR-40', 'DEMO-M', 196.0, 0.19, 5.2, 4.8, True, 18),
    stack('BR-41', 'DEMO-M', 204.0, 0.24, 6.1, 6.6, True, 19),
    stack('BR-42', 'DEMO-M', 212.0, 0.27, 5.6, 5.1, True, 20),
    stack('BR-43', 'DEMO-M', 220.0, 0.31, 7.0, 7.4, True, 21),
    stack('BR-44', 'DEMO-M', 188.0, 0.15, 4.6, 4.2, True, 22),
    stack('BR-45', 'DEMO-M', 232.0, 0.36, 8.2, 8.8, True, 23),
    stack('BR-46', 'DEMO-M', 200.0, 0.22, 5.9, 5.5, True, 24),
    stack('BR-47', 'DEMO-M', 216.0, 0.29, 6.8, 7.1, True, 25),
    stack('BR-48', 'DEMO-M', 192.0, 0.18, 5.0, 4.6, True, 26),
    stack('BR-49', 'DEMO-M', 224.0, 0.33, 7.6, 8.1, True, 27),
    stack('BR-50', 'DEMO-M', 208.0, 0.25, 6.4, 6.9, True, 28),
    stack('BR-51', 'DEMO-M', 198.0, 0.21, 5.3, 4.9, True, 29),
]

FIXTURES = [
    (demolitions, [{'code': 'DEMO-K',
  'street': '西汀渡口旧房',
  'survey': 'SX-431',
  'load_grade': '饰面',
  'allowed': True},
 {'code': 'DEMO-L',
  'street': '北桥附楼',
  'survey': 'SX-433',
  'load_grade': '墙芯',
  'allowed': True},
 {'code': 'DEMO-M',
  'street': '南仓车队棚',
  'survey': 'SX-437',
  'load_grade': '饰面',
  'allowed': True}]),
    (brick_stacks, LEGACY + PENDING + POOL),
    (rack_candidates, [{'code': 'COMP-1',
  'member': 'BR-00',
  'pair': 'BR-06',
  'cluster_size': 5,
  'token': 'c-seed'}]),
    (rack_merges, [{'code': 'PACK-0',
  'candidate': 'COMP-1',
  'rack': 'X-7',
  'pieces': 36,
  'operator_note': '备样教学架'}]),
]
