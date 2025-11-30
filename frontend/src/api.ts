import type { GroupSummary, Question, Scoreboard } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE || "";

async function request<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!response.ok) {
    const detail = await response
      .json()
      .catch(() => ({ detail: response.statusText }));
    throw new Error(detail.detail || "请求失败");
  }

  return response.json();
}

export async function fetchGroups(): Promise<GroupSummary[]> {
  const data = await request<{ groups: GroupSummary[] }>("/api/groups");
  return data.groups;
}

export async function spinGroup(exclude: string[]): Promise<string> {
  const data = await request<{ group: string }>("/api/spin-group", {
    method: "POST",
    body: JSON.stringify({ excludeGroups: exclude }),
  });
  return data.group;
}

export async function spinQuestion(
  group: string,
  excludeQuestionIds: string[],
): Promise<Question> {
  return request<Question>("/api/spin-question", {
    method: "POST",
    body: JSON.stringify({ group, excludeQuestionIds }),
  });
}

interface GradeResult {
  score: number;
  feedback: string;
  question: Question;
  scoreboard: Scoreboard;
}

export async function gradeAnswer(
  params: {
    questionId: string;
    userName?: string;
    userAnswer: string;
    currentScore: number;
  },
): Promise<GradeResult> {
  return request<GradeResult>("/api/grade-answer", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

