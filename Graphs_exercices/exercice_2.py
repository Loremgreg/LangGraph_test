from typing import TypedDict, List
from langgraph.graph import StateGraph 
import math 

class AgentState(TypedDict):
    name: str
    value: List[int]
    operation: str
    result: str

 def calculus(state: AgentState) -> AgentState:
    """Node that add or multiply element"""
    if state["operation"] == "*":
        state["result"] = f"Hi,  {state['name']}, your answer is {math.prod(state["value"])}"
    elif state["operation"] == "+":
        state["result"] = f"Hi,  {state['name']}, your answer is {sum(state["value"])}"
    else:
        state["result"] = "invalid mon coco!"
        
    
    
    return state

    
graph = StateGraph(AgentState)
graph.add_node("final", calculus)
graph.set_entry_point("final")
graph.set_finish_point("final")

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

answer = app.invoke({"name": "Leonidas", "value": [2, 3, 5], "operation": "*"})

print(answer["result"])