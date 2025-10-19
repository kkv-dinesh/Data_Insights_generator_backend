# analysis.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.data_processor import process_data_and_analyze
from services.ai_generator import generate_insights
import schemas

router = APIRouter()


@router.post("/upload", response_model=schemas.AnalysisResult)
async def upload_dataset_and_analyze(file: UploadFile = File(...)):
    """
    Accepts a dataset file (CSV/Excel), analyzes it statistically,
    generates visualizations, and uses AI to create a summary report.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Read file content
    try:
        file_content = await file.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not read file content.")

    # 1. Data processing
    try:
        statistical_facts_for_ai, visualizations, full_stat_data = process_data_and_analyze(
            file_content, file.filename
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during data processing: {e}")

    # 2. Generate AI summary
    try:
        summary_report = generate_insights(statistical_facts_for_ai)
    except Exception as e:
        print(f"AI generation error: {e}")
        summary_report = "Could not generate AI insights due to an internal error."

    # 3. Return results
    return schemas.AnalysisResult(
        summary_report=summary_report,
        statistical_metrics=full_stat_data,
        visualizations=visualizations
    )
