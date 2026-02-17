from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from graph_store import ContextGraph
from llm import generate_response
from baseline import baseline_response
from vector_store import SimpleVectorStore
from rich import print

class GraphState(BaseModel):
    user_id: str
    user_message: str
    context: dict = {}
    retrieved_docs: list = []
    response: str = ""


context_graph = ContextGraph()
vector_store = SimpleVectorStore()

def create_user_if_not_exists(user_id):

    if not context_graph.node_exists(user_id):

        name = input("Enter user name: ")
        role = input("Enter role (Student/Parent/Counselor): ")
        goal = input("Enter current goal: ")
        screen = input("Enter current screen: ")
        course = input("Enter course name: ")

        context_graph.add_node(user_id, "User", name=name)

        role_id = f"role_{user_id}"
        goal_id = f"goal_{user_id}"
        screen_id = f"screen_{user_id}"
        course_id = f"course_{user_id}"

        context_graph.add_node(role_id, "Role", value=role)
        context_graph.add_node(goal_id, "Goal", title=goal)
        context_graph.add_node(screen_id, "Screen", name=screen)
        context_graph.add_node(course_id, "Course", name=course)

        context_graph.add_edge(user_id, role_id, "HAS_ROLE")
        context_graph.add_edge(user_id, goal_id, "WORKING_ON")
        context_graph.add_edge(user_id, screen_id, "CURRENT_SCREEN")
        context_graph.add_edge(goal_id, course_id, "RELATED_TO")


def retrieve_context(state: GraphState):

    subgraph = context_graph.get_user_context_subgraph(state.user_id)

    state.context = subgraph

    state.retrieved_docs = vector_store.search(
        state.user_message
    )

    return state


def build_prompt(state: GraphState):

    prompt = f"""
You are an intelligent SaaS AI assistant.

User Message:
{state.user_message}

User Context Graph:
{state.context}

Relevant Knowledge:
{state.retrieved_docs}

Generate a helpful, personalized response.
"""

    state.response = generate_response(prompt)

    return state


def store_conversation(state: GraphState):

    msg_id = f"msg_{hash(state.user_message)}"
    res_id = f"res_{hash(state.response)}"

    context_graph.add_node(msg_id, "Message", text=state.user_message)

    context_graph.add_node(res_id, "Response", text=state.response)

    context_graph.add_edge(state.user_id, msg_id, "SENT")
    context_graph.add_edge(msg_id, res_id, "GENERATED")

    return state



workflow = StateGraph(GraphState)

workflow.add_node("retrieve_context", retrieve_context)

workflow.add_node("build_prompt", build_prompt)

workflow.add_node("store_conversation", store_conversation)

workflow.set_entry_point("retrieve_context")

workflow.add_edge("retrieve_context", "build_prompt")

workflow.add_edge("build_prompt", "store_conversation")

workflow.add_edge("store_conversation", END)

app = workflow.compile()

def chat():

    user_id = input("Enter user ID: ")

    create_user_if_not_exists(user_id)

    print("\nAI Assistant Ready. Type 'exit' to quit.\n")

    while True:

        user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        print("\n--- BASELINE ---")

        print(baseline_response(user_message))

        print("\n--- CONTEXT GRAPH ---")

        result = app.invoke({
            "user_id": user_id,
            "user_message": user_message
        })

        print("AI:", result["response"])

        print("\n")


if __name__ == "__main__":

    vector_store.add_text(
        "Assignments require regression, classification, and evaluation."
    )

    vector_store.add_text(
        "Students should review lectures, datasets, and deadlines."
    )

    chat()

