from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

config = {
    "runtime": "vercel-python@3.11"
}

from backend.logic import (
    get_question_by_id,
    list_groups,
    random_group,
    random_question,
    score_with_special_tiles,
)
from backend.openrouter import OpenRouterError, grade_answer

app = FastAPI(title="Spin The Wheel API", config=config)


class SpinGroupRequest(BaseModel):
    excludeGroups: Optional[List[str]] = Field(default=None, description="Group ids to skip")


class SpinGroupResponse(BaseModel):
    group: str


class SpinQuestionRequest(BaseModel):
    group: str
    excludeQuestionIds: Optional[List[str]] = None


class QuestionResponse(BaseModel):
    id: str
    group: str
    prompt: str


class GradeRequest(BaseModel):
    questionId: str
    userName: Optional[str] = None
    userAnswer: str
    currentScore: int = 0


class GradeResponse(BaseModel):
    score: int
    feedback: str
    question: QuestionResponse
    scoreboard: dict


@app.get("/api/health")
def healthcheck():
    return {"status": "ok"}


@app.get("/api/groups")
def get_groups():
    return {"groups": list_groups()}


@app.post("/api/spin-group", response_model=SpinGroupResponse)
def spin_group(payload: SpinGroupRequest):
    try:
        group = random_group(payload.excludeGroups)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"group": group}


@app.post("/api/spin-question", response_model=QuestionResponse)
def spin_question(payload: SpinQuestionRequest):
    try:
        question = random_question(payload.group, payload.excludeQuestionIds)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "id": question.id,
        "group": question.group,
        "prompt": question.prompt,
    }


@app.post("/api/grade-answer", response_model=GradeResponse)
def grade(payload: GradeRequest):
    try:
        question = get_question_by_id(payload.questionId)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not payload.userAnswer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    try:
        grading = grade_answer(
            question=question.prompt,
            standard_answer=question.answer,
            user_answer=payload.userAnswer,
        )
    except OpenRouterError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    scoreboard = score_with_special_tiles(payload.currentScore, grading["score"])

    return {
        "score": grading["score"],
        "feedback": grading["feedback"],
        "question": {
            "id": question.id,
            "group": question.group,
            "prompt": question.prompt,
        },
        "scoreboard": scoreboard,
    }

