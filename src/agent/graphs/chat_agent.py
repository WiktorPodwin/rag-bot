from src.agent.graphs.states import GraphState, GraphInputState, GraphOutputState
from src.agent.graphs.nodes import parse_to_messages, call

from langgraph.graph import StateGraph

workflow = StateGraph(GraphState, input=GraphInputState, output=GraphOutputState)

workflow.add_node(parse_to_messages.__name__, parse_to_messages)
workflow.add_node(call.__name__, call)

workflow.add_edge("__start__", parse_to_messages.__name__)
workflow.add_edge(parse_to_messages.__name__, call.__name__)
workflow.add_edge(call.__name__, "__end__")

agent = workflow.compile()
