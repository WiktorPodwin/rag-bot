from langgraph.graph.message import add_messages
from operator import add

from pydantic import BaseModel, Field
from typing import Annotated, Sequence


class GraphInputState(BaseModel):
    query: str


GraphInputState.model_rebuild()


class GraphOutputState(BaseModel):
    messages: Annotated[Sequence, add_messages] = Field(default_factory=list)


GraphOutputState.model_rebuild()


class GraphState(GraphInputState, GraphOutputState):
    pass


GraphState.model_rebuild()

# class GraphState(GraphInputState):
#     messages: Annotated[Sequence, add]


# class GraphOutputState(BaseModel):
#     messages: Annotated[Sequence, add]
