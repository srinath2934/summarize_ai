# ── Summarize AI — Core Engine ───────────────────────────────
# LangGraph + Pydantic + Groq (Llama 3.3 70B)
# ─────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing import TypedDict, Optional
from langgraph.checkpoint.memory import MemorySaver

# ── Config ───────────────────────────────────────────────────
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "env", ".env"))


# ── Pydantic Output Schema ──────────────────────────────────
class SummaryOutput(BaseModel):
    """Structured JSON output the LLM must return."""
    title: str = Field(description="Short descriptive title for the text")
    summary: str = Field(description="2-3 sentence summary")
    key_points: list[str] = Field(description="3-5 key takeaways")


# ── Graph State ──────────────────────────────────────────────
class GraphState(TypedDict):
    """Data flowing through the graph nodes."""
    input_text: str
    summary_output: Optional[SummaryOutput]
    error: Optional[str]
    history: list[dict]


# ── LLM Setup ───────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)
structured_llm = llm.with_structured_output(SummaryOutput)


# ── Node: Summarize ─────────────────────────────────────────
def summarize_node(state: GraphState) -> dict:
    """Process input text and return structured summary."""
    input_text = state["input_text"]
    history = state.get("history", [])

    try:
        messages = [
            ("system", "You are an expert text summarizer. Provide a title, "
             "concise summary, 3-5 key points, sentiment, and word count."),
        ]

        # Append conversation history for memory context
        for msg in history:
            messages.append((msg["role"], msg["content"]))

        messages.append(("human", f"Summarize this text:\n\n{input_text}"))

        result = structured_llm.invoke(messages)

        new_history = history + [
            {"role": "human", "content": f"Summarize: {input_text[:200]}..."},
            {"role": "assistant", "content": result.summary}
        ]

        return {"summary_output": result, "error": None, "history": new_history}

    except Exception as e:
        return {"summary_output": None, "error": str(e), "history": history}


# ── Build Graph ──────────────────────────────────────────────
graph_builder = StateGraph(GraphState)
graph_builder.add_node("summarize", summarize_node)
graph_builder.add_edge(START, "summarize")
graph_builder.add_edge("summarize", END)

# Persistent memory across invocations
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)


# ── Public API ───────────────────────────────────────────────
def run_summarizer(text: str, thread_id: str = "default") -> dict:
    """Run the summarizer graph and return structured output."""
    config = {"configurable": {"thread_id": thread_id}}

    result = graph.invoke(
        {"input_text": text, "summary_output": None, "error": None, "history": []},
        config=config
    )

    if result.get("error"):
        return {"error": result["error"]}

    s = result["summary_output"]
    return {
        "title": s.title,
        "summary": s.summary,
        "key_points": s.key_points
    }


# ── Local Test ───────────────────────────────────────────────
if __name__ == "__main__":
    test_text = """
    Artificial intelligence is transforming healthcare in remarkable ways.
    From early disease detection to personalized treatment plans, AI algorithms
    are helping doctors make better decisions. Machine learning models can now
    analyze medical images with accuracy rivaling experienced radiologists.
    However, concerns about data privacy and algorithmic bias remain challenges.
    """

    print("🔄 Running Summarizer...")
    result = run_summarizer(test_text, thread_id="test-1")

    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"📌 Title:     {result['title']}")
        print(f"📝 Summary:   {result['summary']}")
        print(f"📊 Sentiment: {result['sentiment']}")
        print(f"🔢 Words:     {result['word_count']}")
        print(f"🔑 Key Points:")
        for i, p in enumerate(result['key_points'], 1):
            print(f"   {i}. {p}")