import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
import json
import re
import pandas as pd
import numpy as np
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from utils.llm_factory import stream_with_fallback, invoke_with_fallback


SYSTEM = """You are a Professional Data Analysis Agent.

BEHAVIOR:
- Think like a professional data analyst
- Always: understand → analyze → give insights → recommend
- Sound human and clear, not robotic
- Simulate calculations logically if needed

When user asks for a VISUALIZATION, output EXACTLY this JSON block (nothing else):
```tool
{"tool": "plot", "type": "<plot_type>", "x": "<col_or_null>", "y": "<col_or_null>", "hue": "<col_or_null>", "title": "<title>"}
```
plot_type options: histogram, scatter, box, heatmap, bar, line, violin, pairplot

When answering DATA QUESTIONS, follow this format:
Agent Used: Data Analysis Agent

Response:

**Understanding:**
<what you understood about the question>

**Analysis:**
<key findings and statistics>

**Insights:**
<what the data tells us>

**Recommendation:**
<actionable suggestion>"""


def _build_context(df: pd.DataFrame, eda: dict) -> str:
    num_cols = eda.get("num_cols", [])
    sample   = df.head(3).to_string(max_cols=8)
    stats    = ""
    if num_cols:
        try:
            stats = df[num_cols[:6]].describe().round(2).to_string()
        except Exception:
            pass
    return f"""Dataset Info:
- Shape: {df.shape[0]:,} rows × {df.shape[1]} columns
- Numeric columns: {num_cols}
- Categorical columns: {eda.get('cat_cols', [])}
- Missing values: {sum(eda.get('nulls', {}).values())} total
- Duplicates: {eda.get('duplicates', 0)}

Sample (first 3 rows):
{sample}

Statistics:
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

        context  = _build_context(df, eda)
        num_cols = eda.get("num_cols", [])
        cat_cols = eda.get("cat_cols", [])

        msgs = [SystemMessage(content=SYSTEM),
                HumanMessage(content=f"Dataset context:\n{context}")]

        for h in history[-8:]:
            if h["role"] == "user":
                msgs.append(HumanMessage(content=h["content"]))
            else:
                msgs.append(AIMessage(content=h["content"]))
        msgs.append(HumanMessage(content=message))

        # Check if user wants a visualization
        viz_kw = ["plot", "chart", "graph", "visuali", "histogram", "scatter",
                  "bar", "line", "heatmap", "distribution", "show me", "draw",
                  "display", "correlation map", "violin", "boxplot"]
        wants_viz = any(k in message.lower() for k in viz_kw)

        if wants_viz:
            full = invoke_with_fallback(msgs, temperature=0.1)

            # Try to extract tool JSON
            tool_match = re.search(r"```tool\s*(\{.*?\})\s*```", full, re.DOTALL)
            if tool_match:
                try:
                    yield json.loads(tool_match.group(1))
                    return
                except json.JSONDecodeError:
                    pass

            # Auto-infer plot from message
            plot_type = "histogram"
            for pt in ["scatter", "bar", "line", "heatmap", "box",
                       "violin", "pairplot", "histogram"]:
                if pt in message.lower():
                    plot_type = pt
                    break

            x_col, y_col = None, None
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
                "tool": "plot", "type": plot_type,
                "x": x_col, "y": y_col, "hue": None,
                "title": f"{plot_type.title()} — {x_col or 'Data'}",
            }
            return

        # Regular Q&A — stream structured response
        yield from stream_with_fallback(msgs, temperature=0.4)
