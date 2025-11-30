export interface GroupSummary {
    id: string;
    label: string;
    questionCount: number;
}
export interface Question {
    id: string;
    group: string;
    prompt: string;
}
export interface SpecialEvent {
    type: "forward" | "backward";
    steps: number;
    message: string;
}
export interface Scoreboard {
    score: number;
    hasWinner: boolean;
    specialEvent: SpecialEvent | null;
}
