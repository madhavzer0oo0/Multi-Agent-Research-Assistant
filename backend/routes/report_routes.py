import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import ReportHistory, User
from backend.schemas import ReportCreate, ReportGenerateOut, ReportOut


router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportGenerateOut, status_code=status.HTTP_201_CREATED)
def generate_report(
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        from agents.coordinator_agent import Coordinator

        coordinator = Coordinator(payload.topic)
        report_text = coordinator.run(max_results=payload.max_results)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Search service error: {exc}",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    report = ReportHistory(
        user_id=current_user.id,
        topic=payload.topic,
        report=report_text,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return ReportGenerateOut(status="success", report=report)


@router.get("", response_model=list[ReportOut])
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(ReportHistory)
        .filter(ReportHistory.user_id == current_user.id)
        .order_by(ReportHistory.created_at.desc())
        .all()
    )


@router.get("/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    report = _get_user_report(db, current_user.id, report_id)
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    report = _get_user_report(db, current_user.id, report_id)
    db.delete(report)
    db.commit()
    return None


def _get_user_report(db: Session, user_id: int, report_id: int) -> ReportHistory:
    report = (
        db.query(ReportHistory)
        .filter(ReportHistory.id == report_id, ReportHistory.user_id == user_id)
        .first()
    )
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )
    return report
