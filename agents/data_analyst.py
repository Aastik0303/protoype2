import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import json
import pandas as pd
import numpy as np
from langchain.schema import HumanMessage, SystemMessage
from utils.llm_factory import stream_with_fallback, invoke_with_fallback


SYSTEM = """You are an expert data analyst with access to a dataset.
The user will ask questions about the data. You can:
1. Answer questions about the data directly
2. Request a visualization by outputting a JSON tool call
3. Perform EDA and statistical analysis

When the user asks for a chart/plot/visualization, respond with EXACTLY this JSON (nothing else before or after):
```tool
{"tool": "plot", "type": "<plot_type>", "x": "<col_or_null>", "y": "<col_or_null>", "hue": "<col_or_null>", "title": "<title>"}
```
plot_type options: histogram, scatter, box, heatmap, bar, line, violin, pairplot

When the user asks for statistics or data info, just answer directly in markdown.
Be concise, insightful, and data-driven in all responses."""


def _build_context(df: pd.DataFrame, eda: dict) -> str:
    num_cols = eda.get("num_cols", [])
    cat_cols = eda.get("cat_cols", [])
    sample = df.head(3).to_string(max_cols=8)
    stats = ""
    if num_cols:
        try:
            stats = df[num_cols[:6]].describe().round(2).to_string()
        except Exception:
            pass
    return f"""Dataset Overview:
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Numeric columns: {num_cols}
- Categorical columns: {cat_cols}
- Missing values: {sum(eda.get('nulls', {}).values())} total
- Duplicates: {eda.get('duplicates', 0)}

First 3 rows:
{sample}

Statistical Summary:
{stats}"""


class DataAnalystAgent:
    NAME = "Data Analyst"
    ICON = "📊"
    MODEL_TAG = "Gemini/Groq + Data Tools"

    def stream_with_data(
        self,
        message: str,
        history: list,
        df: pd.DataFrame,
        eda: dict,
    ) -> Generator[str | dict, None, None]:
        """
        Yields either str chunks or dict tool calls.
        dict format: {"tool": "plot", "type": ..., "x": ..., "y": ..., "hue": ..., "title": ...}
        """
        context = _build_context(df, eda)

        msgs = [
            SystemMessage(content=SYSTEM),
            HumanMessage(content=f"Dataset context:\n{context}"),
        ]
        for h in history[-8:]:
            from langchain.schema import AIMessage
            if h["role"] == "user":
                msgs.append(HumanMessage(content=h["content"]))
            else:
                msgs.append(AIMessage(content=h["content"]))
        msgs.append(HumanMessage(content=message))

        # Check if user is asking for a visualization
        viz_keywords = ["plot", "chart", "graph", "visuali", "histogram",
                        "scatter", "bar chart", "line chart", "heatmap",
                        "distribution", "show me", "draw", "display"]
        wants_viz = any(k in message.lower() for k in viz_keywords)

        if wants_viz:
            # Use invoke to get full response for tool call parsing
            full = invoke_with_fallback(msgs, temperature=0.1)

            # Try to extract tool call JSON
            import re
            tool_match = re.search(r"```tool\s*(\{.*?\})\s*```", full, re.DOTALL)
            if tool_match:
                try:
                    tool_call = json.loads(tool_match.group(1))
                    yield tool_call  # dict — caller handles plotting
                    return
                except json.JSONDecodeError:
                    pass

            # If no valid tool call, try to infer from message
            plot_type = "histogram"
            for pt in ["scatter", "bar", "line", "heatmap", "box", "violin", "pairplot", "histogram"]:
                if pt in message.lower():
                    plot_type = pt
                    break

            # Guess columns from message
            num_cols = eda.get("num_cols", [])
            cat_cols = eda.get("cat_cols", [])
            x_col = None
            y_col = None
            for col in df.columns:
                if col.lower() in message.lower():
                    if x_col is None:
                        x_col = col
                    elif y_col is None:
                        y_col = col
            if x_col is None and num_cols:
                x_col = num_cols[0]
            if y_col is None and len(num_cols) > 1:
                y_col = num_cols[1]

            yield {
                "tool": "plot",
                "type": plot_type,
                "x": x_col,
                "y": y_col,
                "hue": None,
                "title": f"{plot_type.title()} — {x_col or 'Data'}",
            }
            return

        # Regular Q&A — stream response
        yield from stream_with_fallback(msgs, temperature=0.4)
