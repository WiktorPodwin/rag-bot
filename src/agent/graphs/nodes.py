from src.agent.graphs.states import GraphState

from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage
from src.agent.rag_components import llm, chat_prompt, tools, tools_map

from typing import Dict, List


llm_w_tools = llm.bind_tools(tools, tool_choice="retriever")


def parse_to_messages(state: GraphState) -> Dict[str, List[AnyMessage]]:
    query = state.query
    messages = state.messages

    if not messages:
        messages.extend(chat_prompt.format_messages())

    if isinstance(query, str):
        messages.append(HumanMessage(content=query))

    return {"messages": messages}


async def call(state: GraphState) -> Dict[str, List[AnyMessage]]:
    messages = state.messages

    response = await llm_w_tools.ainvoke(messages)
    messages.append(response)

    if tool_calls := response.tool_calls:
        for tool_call in tool_calls:
            tool = tools_map.get(tool_call["name"])
            tool_message = await tool.ainvoke(tool_call)

            if not tool_message.content:
                tool_message.content = ""

            messages.append(tool_message)

        final_response = await llm.ainvoke(messages)
        messages.append(final_response)

    return {"messages": messages}
