import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]      #Store humanM and AiM 

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))  # reponse.content extract de content part of the response (exclus le non necessaire comme le nombre de token, etc) 
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ", state["messages"])

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()


conversation_history = []                                          # Memory 

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})       # l'agent invoqué est graph.compile()
    conversation_history = result["messages"]
    user_input = input("Enter: ")
                                                                    
# Quand on sort de la convers avec "exit", llm oublie les infos precedente -> solution = storer dans une database. Mais ici on prototype donc on store ca dans ce code:
with open("logging.txt", "w") as file:                  # crée un file logging.txt dans lequel il peut writting 
    file.write("Your Conversation Log:\n")
    
    for message in conversation_history:                # pour tous les msg dans la convers histo
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")