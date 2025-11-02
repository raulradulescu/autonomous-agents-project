from typing import NamedTuple, NewType

NodeId = NewType("NodeId", int)


class Interaction(NamedTuple):
    step: int
    src_agent: str
    dst_node: int
    action: str
    success: int  # 0/1 for CSV friendliness

