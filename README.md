# Bridge-It: Context-Aware AI Assistant

## Overview
Bridge-It is a context-aware AI chatbot designed to provide personalized, relevant, and consistent responses by leveraging a dynamic context graph and a vector-based knowledge store. The system is modular, extensible, and built for educational and productivity use cases.

## Architecture

### Main Components

- **app.py**: Entry point; orchestrates the workflow, user interaction, and graph-based context management.
- **graph_store.py**: Implements the `ContextGraph` class for storing and querying user context as a property graph (nodes and edges).
- **vector_store.py**: Implements a simple vector store for semantic search over knowledge snippets.
- **llm.py**: Handles LLM-based response generation.
- **baseline.py**: Provides a baseline (non-contextual) response for comparison.

### Workflow
1. **User Initialization**: On first interaction, user profile, role, goal, screen, and course are added to the context graph.
2. **Message Handling**: For each user message:
   - The user's context subgraph is retrieved.
   - Relevant knowledge is retrieved from the vector store using semantic search.
   - A prompt is constructed combining the user message, context graph, and relevant knowledge.
   - The LLM generates a response based on this prompt.
   - The conversation (message and response) is stored in the context graph for traceability.

### Design Decisions
- **Context Graph**: Chosen for its flexibility in representing complex, evolving user states and relationships (e.g., roles, goals, screens, courses). Enables fine-grained, structured context retrieval.
- **Vector Store**: Complements the graph by providing unstructured, semantic knowledge retrieval for open-ended queries.
- **Modular Nodes**: Each workflow step (context retrieval, prompt building, response generation, conversation storage) is a separate function, making the system easy to extend or modify.
- **Baseline Comparison**: Including a baseline response highlights the value added by context-aware reasoning.

## How the Context Graph Improves Response Quality

- **Personalization**: The graph encodes user-specific information (e.g., current goal, course, screen), allowing the assistant to tailor responses to the user's situation.
- **Relevance**: By retrieving only the subgraph relevant to the current user, the assistant focuses on contextually appropriate information, reducing generic or off-topic answers.
- **Consistency**: Storing conversation history and user state in the graph ensures that the assistant can maintain continuity across multiple interactions, referencing past goals, roles, or actions.
- **Extensibility**: New node/edge types (e.g., achievements, preferences) can be added without major refactoring, supporting richer context over time.

## Usage

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the assistant:
   ```sh
   python app.py
   ```
3. Follow prompts to create a user and interact with the assistant. Type `exit` to quit.

## Example

- User: "I'm stuck on my assignment. What should I focus on?"
- Assistant (with context): "As a Student working on 'Complete Data Science Assignment' in 'Intro to Data Science', you should review regression and classification concepts, and check the assignment's deadline and rubric."

## License
MIT
