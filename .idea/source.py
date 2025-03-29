from langgraph.graph import StateGraph, END
from pydantic.v1 import compiled
from typing import TypedDict

# Define the state
class BasicState(TypedDict):
    message: str

# Router function: decide next step
def route_from_input(state: BasicState):
    print("Router: Deciding next node...")
    if "Investor" in state["message"]:
        return "hello_investor"
    elif    "Trader" in state["message"]:
        return  "hello_trader"
    else:
        raise ValueError("Unknow role in message. Must include 'Investor' or 'Trader'.")

# Node: Response for investor
    def hello_investor(state: BasicState):
        print("Node: Hello Investor")
        return {"message": state["message"] + " You're a valued investor. Welcome aboard!"}

# Node: Response for trader
def hello_trader(state: BasicState):
    print("Node: Hello Trader")
    return {"message": state["message"] + " Ready to trade? Let's go!"}

# Dummy passthrough for routing node
def passthrough(state: BasicState):
    return state

#Build the graph
basic_workflow = StateGraph(BasicState)

# Add router node
basic_workflow.add_node("router", passthrough)

#Add destination nodes
basic_workflow.add_node("hello_investor", hello_investor)
basic_workflow.add_node("hello_trader", hello_trader)

# Add conditional edges from router ( targets now exist )
basic_workflow.add_conditional_edges("router", route_from_input)

# Connect branches to END
basic_workflow.add_edge("hello_investor", END)
basic_workflow.add_edge("hello_trader", END)

# Set entry point
basic_workflow.set_entry_point("router")

#Compile the graph
compiled = basic_workflow.compile()

# Test with user input
inputs = {"message": "Hello Investor!"}
result = compiled.invoke(inputs)
print(f"Result: {result}")