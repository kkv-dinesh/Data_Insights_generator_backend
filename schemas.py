from pydantic import BaseModel
from typing import Dict, List, Any

class ColumnStatistics(BaseModel):
    mean: float
    median: float
    mode: List[Any]
    std_dev: float

class AnalysisResult(BaseModel):
    summary_report: str
    statistical_metrics: Dict[str, ColumnStatistics]
    visualizations: Dict[str, str]  # Base64 images
