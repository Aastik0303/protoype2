import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import json
import pandas as pd
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from utils.llm import stream, invoke

SYSTEM = """You are a data analyst. The user has uploaded a dataset.
Answer questions about the data clearly.
When user wants a visualization, reply with ONLY this JSON (nothing else before/after the block):
```tool
{"tool":"plot","type":"<histogram|scatter|bar|line|box|heatmap|violin>","x":"<col or null>","y":"<col or null>","title":"<title>"}
```
For data questions, just answer directly in markdown."""


def _ctx(df: pd.DataFrame, eda: dict) -> str:
    nc = eda.get("num_cols", [])
    try:
        stats = df[nc[:5]].describe().round(2).to_string() if nc else ""
    except Exception:
        stats = ""
    return f"""Dataset: {df.shape[0]} rows × {df.shape[1]} cols
Numeric: {eda.get('num_cols',[])}
Categorical: {eda.get('cat_cols',[])}
Nulls: {sum(eda.get('nulls',{}).values())}
Sample:\n{df.head(3).to_string(max_cols=6)}
Stats:\n{stats}"""


def run(message: str, history: list, df: pd.DataFrame, eda: dict):
    ctx  = _ctx(df, eda)
    msgs = [SystemMessage(content=SYSTEM), HumanMessage(content=f"Dataset:\n{ctx}")]

    for h in history[-6:]:
        if h["role"] == "user":
            msgs.append(HumanMessage(content=h["content"]))
        else:
            msgs.append(AIMessage(content=h["content"]))
    msgs.append(HumanMessage(content=message))

    VIZ_KW = ["plot","chart","graph","histogram","scatter","bar","line",
               "heatmap","distribution","visuali","show me","draw","violin","box"]
    wants_viz = any(k in message.lower() for k in VIZ_KW)

    if wants_viz:
        full = invoke(msgs, temperature=0.1)
        m = re.search(r"```tool\s*(\{.*?\})\s*```", full, re.DOTALL)
        if m:
            try:
                yield json.loads(m.group(1))
                return
            except Exception:
                pass
        # Auto-guess plot
        nc = eda.get("num_cols", [])
        pt = "histogram"
        for p in ["scatter","bar","line","heatmap","box","violin"]:
            if p in message.lower():
                pt = p
                break
        x = nc[0] if nc else None
        y = nc[1] if len(nc) > 1 else None
        for col in df.columns:
            if col.lower() in message.lower():
                x = col
                break
        yield {"tool": "plot", "type": pt, "x": x, "y": y, "title": f"{pt.title()} Chart"}
        return

    yield from stream(msgs, temperature=0.4)
