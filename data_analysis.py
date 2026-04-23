import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BG      = "#06111f"
CARD    = "#0d1f3c"
BORDER  = "#1e3a5f"
CYAN    = "#38bdf8"
VIOLET  = "#818cf8"
PINK    = "#f472b6"
GREEN   = "#34d399"
YELLOW  = "#fbbf24"
PALETTE = [CYAN, VIOLET, PINK, GREEN, YELLOW, "#fb923c", "#a78bfa"]


def load_df(file) -> pd.DataFrame:
    name = file.name
    if name.endswith(".xlsx"):
        return pd.read_excel(file)
    if name.endswith(".tsv"):
        return pd.read_csv(file, sep="\t")
    return pd.read_csv(file)


def get_eda(df: pd.DataFrame) -> dict:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return {
        "shape":      df.shape,
        "num_cols":   num_cols,
        "cat_cols":   cat_cols,
        "nulls":      df.isnull().sum().to_dict(),
        "dtypes":     {c: str(t) for c, t in df.dtypes.items()},
        "duplicates": int(df.duplicated().sum()),
        "memory":     f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
        "corr":       df[num_cols].corr().round(3) if len(num_cols) >= 2 else None,
    }


def _style(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)
    ax.tick_params(colors="#94a3b8", labelsize=10)
    ax.xaxis.label.set_color("#94a3b8")
    ax.yaxis.label.set_color("#94a3b8")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)


def make_plot(df: pd.DataFrame, plot_type: str,
              x_col=None, y_col=None, hue_col=None, title=None) -> bytes:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    pt = plot_type.lower().replace(" ", "").replace("_", "")

    fig, ax = plt.subplots(figsize=(10, 5))
    _style(fig, ax)

    try:
        if pt == "histogram" and x_col and x_col in df.columns:
            ax.hist(df[x_col].dropna(), bins=30, color=CYAN, alpha=0.85, edgecolor=BG)
            ax.set_xlabel(x_col); ax.set_ylabel("Frequency")
            ax.set_title(title or f"Distribution — {x_col}")

        elif pt == "scatter" and x_col and y_col and x_col in df.columns and y_col in df.columns:
            if hue_col and hue_col in df.columns:
                for i, cat in enumerate(df[hue_col].dropna().unique()[:8]):
                    mask = df[hue_col] == cat
                    ax.scatter(df.loc[mask, x_col], df.loc[mask, y_col],
                               color=PALETTE[i % len(PALETTE)], label=str(cat), alpha=0.7, s=40)
                ax.legend(facecolor=CARD, edgecolor=BORDER, labelcolor="#e2e8f0", fontsize=9)
            else:
                ax.scatter(df[x_col], df[y_col], color=CYAN, alpha=0.7, s=40)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(title or f"{x_col} vs {y_col}")

        elif pt == "boxplot" or pt == "box":
            cols = [c for c in (num_cols[:8])]
            data = [df[c].dropna().values for c in cols]
            bp = ax.boxplot(data, patch_artist=True)
            for i, patch in enumerate(bp["boxes"]):
                patch.set_facecolor(PALETTE[i % len(PALETTE)])
                patch.set_alpha(0.8)
            for el in ["whiskers", "caps", "medians"]:
                for item in bp[el]:
                    item.set(color="#94a3b8", linewidth=1.5)
            ax.set_xticks(range(1, len(cols) + 1))
            ax.set_xticklabels(cols, rotation=30, ha="right")
            ax.set_title(title or "Box Plot")

        elif pt in ["heatmap", "correlationheatmap", "correlation"]:
            plt.close(fig)
            n = max(7, len(num_cols))
            fig, ax = plt.subplots(figsize=(n, n - 1))
            _style(fig, ax)
            corr = df[num_cols].corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                        linewidths=0.5, linecolor=BG,
                        annot_kws={"color": "white", "size": 9})
            ax.set_title(title or "Correlation Heatmap", color="white")

        elif pt in ["bar", "barchart"] and x_col and x_col in df.columns:
            y = y_col if y_col and y_col in df.columns else (num_cols[0] if num_cols else None)
            if y:
                agg = df.groupby(x_col)[y].mean().sort_values(ascending=False).head(20)
                bars = ax.bar(range(len(agg)), agg.values, color=CYAN, alpha=0.85)
                for bar, val in zip(bars, agg.values):
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.01 * (agg.max() or 1),
                            f"{val:.1f}", ha="center", va="bottom",
                            color="#94a3b8", fontsize=8)
                ax.set_xticks(range(len(agg)))
                ax.set_xticklabels(agg.index, rotation=40, ha="right")
                ax.set_ylabel(y)
                ax.set_title(title or f"Avg {y} by {x_col}")

        elif pt in ["line", "linechart"] and x_col and y_col and x_col in df.columns and y_col in df.columns:
            s = df.sort_values(x_col)
            ax.plot(s[x_col], s[y_col], color=CYAN, linewidth=2)
            ax.fill_between(s[x_col], s[y_col], alpha=0.12, color=CYAN)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(title or f"{y_col} over {x_col}")

        elif pt == "violin":
            cols = num_cols[:6]
            data = [df[c].dropna().values for c in cols]
            if data:
                parts = ax.violinplot(data, showmeans=True, showmedians=True)
                for i, pc in enumerate(parts["bodies"]):
                    pc.set_facecolor(PALETTE[i % len(PALETTE)])
                    pc.set_alpha(0.75)
                ax.set_xticks(range(1, len(cols) + 1))
                ax.set_xticklabels(cols, rotation=30, ha="right")
                ax.set_title(title or "Violin Plot")

        elif pt == "pairplot":
            plt.close(fig)
            cols = num_cols[:5]
            pair_df = df[cols].dropna()
            g = sns.pairplot(pair_df, plot_kws={"color": CYAN, "alpha": 0.5},
                             diag_kws={"color": VIOLET})
            g.fig.patch.set_facecolor(BG)
            for ax2 in g.axes.flatten():
                if ax2:
                    ax2.set_facecolor(CARD)
                    ax2.tick_params(colors="#94a3b8")
            buf = io.BytesIO()
            g.fig.savefig(buf, format="png", bbox_inches="tight", dpi=120, facecolor=BG)
            plt.close()
            buf.seek(0)
            return buf.read()

        else:
            # Fallback: auto histogram of first numeric col
            if num_cols:
                col = x_col if x_col and x_col in num_cols else num_cols[0]
                ax.hist(df[col].dropna(), bins=30, color=CYAN, alpha=0.85, edgecolor=BG)
                ax.set_xlabel(col); ax.set_ylabel("Frequency")
                ax.set_title(title or f"Distribution — {col}")

    except Exception as e:
        ax.text(0.5, 0.5, f"Plot error:\n{e}", transform=ax.transAxes,
                ha="center", va="center", color="#f87171", fontsize=12)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
