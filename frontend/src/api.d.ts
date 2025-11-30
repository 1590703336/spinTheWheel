import type { GroupSummary, Question, Scoreboard } from "./types";
export declare function fetchGroups(): Promise<GroupSummary[]>;
export declare function spinGroup(exclude: string[]): Promise<string>;
export declare function spinQuestion(group: string, excludeQuestionIds: string[]): Promise<Question>;
interface GradeResult {
    score: number;
    feedback: string;
    question: Question;
    scoreboard: Scoreboard;
}
export declare function gradeAnswer(params: {
    questionId: string;
    userName?: string;
    userAnswer: string;
    currentScore: number;
}): Promise<GradeResult>;
export {};
