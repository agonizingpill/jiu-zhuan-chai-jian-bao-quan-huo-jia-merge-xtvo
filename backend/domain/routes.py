from domain.demolitions_api import router as demolitions
from domain.brick_stacks_api import router as brick_stacks
from domain.yard_api import router as yard
from domain.rack_candidates_api import router as rack_candidates
from domain.rack_merges_api import router as rack_merges

routers = (demolitions, brick_stacks, yard, rack_candidates, rack_merges,)
