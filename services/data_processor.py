# data_processor.py
import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Any, List
import schemas

# Built-in Matplotlib style
plt.style.use("ggplot")


def process_data_and_analyze(
    file_content: bytes,
    filename: str,
    selected_columns: List[str] = None
) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, schemas.ColumnStatistics]]:
    """
    Reads CSV/Excel file, computes statistics, generates multiple visualizations.
    Returns:
        facts_for_ai: dict of stats for AI summary
        visualizations: dict of base64-encoded charts
        full_stats: dict of ColumnStatistics
    """
    try:
        # Read CSV or Excel
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file type. Use CSV or Excel.")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    # Filter columns if specified
    if selected_columns:
        df = df[selected_columns]

    facts_for_ai = {}
    visualizations = {}
    full_stats = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            series = df[col].dropna()
            if series.empty:
                continue

            # Stats
            mean = series.mean()
            median = series.median()
            mode_values = series.mode().tolist()[:2]  # top 2 modes
            std_dev = series.std()
            count = len(series)
            min_val = series.min()
            max_val = series.max()
            dtype = str(series.dtype)

            full_stats[col] = schemas.ColumnStatistics(
                mean=mean,
                median=median,
                mode=mode_values,
                std_dev=std_dev
            )

            facts_for_ai[col] = {
                "dtype": dtype,
                "count": count,
                "mean": round(mean, 2),
                "median": round(median, 2),
                "mode": mode_values,
                "std_dev": round(std_dev, 2),
                "min": min_val,
                "max": max_val,
                "has_pie": series.nunique() <= 10
            }

            # Sample for large datasets
            series_to_plot = series.sample(1000, random_state=42) if len(series) > 1000 else series

            # Histogram
            plt.figure(figsize=(6, 4))
            series_to_plot.plot(kind="hist", bins=10, color="skyblue")
            plt.title(f"Histogram of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            plt.close()
            visualizations[f"{col}_hist"] = base64.b64encode(buf.getvalue()).decode("utf-8")

            # Line plot
            plt.figure(figsize=(6, 4))
            series_to_plot.reset_index(drop=True).plot(kind="line", marker="o", color="green")
            plt.title(f"Line Plot of {col}")
            plt.xlabel("Index")
            plt.ylabel(col)
            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            plt.close()
            visualizations[f"{col}_line"] = base64.b64encode(buf.getvalue()).decode("utf-8")

            # Pie chart if ≤10 unique values
            if series.nunique() <= 10:
                plt.figure(figsize=(6, 4))
                series.value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
                plt.title(f"Pie Chart of {col}")
                plt.ylabel("")
                plt.tight_layout()
                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                plt.close()
                visualizations[f"{col}_pie"] = base64.b64encode(buf.getvalue()).decode("utf-8")

    return facts_for_ai, visualizations, full_stats
