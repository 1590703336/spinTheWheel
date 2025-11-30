import { useEffect, useMemo, useState } from "react";
import {
  fetchGroups,
  gradeAnswer,
  spinGroup,
  spinQuestion,
} from "./api";
import type { GroupSummary, Question, Scoreboard } from "./types";
import "./App.css";

type Phase = "idle" | "group" | "question" | "grading";

function App() {
  const [groups, setGroups] = useState<GroupSummary[]>([]);
  const [loadingGroups, setLoadingGroups] = useState(false);
  const [phase, setPhase] = useState<Phase>("idle");
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [usedGroups, setUsedGroups] = useState<string[]>([]);
  const [question, setQuestion] = useState<Question | null>(null);
  const [usedQuestions, setUsedQuestions] = useState<string[]>([]);
  const [userName, setUserName] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [scoreboard, setScoreboard] = useState<Scoreboard>({
    score: 0,
    hasWinner: false,
    specialEvent: null,
  });
  const [feedback, setFeedback] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoadingGroups(true);
      try {
        const data = await fetchGroups();
        setGroups(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoadingGroups(false);
      }
    };
    load();
  }, []);

  const handleSpinGroup = async () => {
    setError(null);
    setFeedback(null);
    setQuestion(null);
    setUserAnswer("");

    try {
      setPending(true);
      const group = await spinGroup(usedGroups);
      setSelectedGroup(group);
      setPhase("group");
      setUsedGroups((prev) =>
        prev.includes(group) ? prev : [...prev, group],
      );
      setUsedQuestions([]);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setPending(false);
    }
  };

  const handleSpinQuestion = async () => {
    if (!selectedGroup) {
      setError("请先抽取一个分组。");
      return;
    }

    try {
      setPending(true);
      const q = await spinQuestion(selectedGroup, usedQuestions);
      setQuestion(q);
      setPhase("question");
      setUsedQuestions((prev) => [...prev, q.id]);
      setFeedback(null);
      setUserAnswer("");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setPending(false);
    }
  };

  const handleGrade = async () => {
    if (!question) {
      setError("请先抽取问题。");
      return;
    }
    if (!userAnswer.trim()) {
      setError("请输入答案。");
      return;
    }

    try {
      setPending(true);
      setError(null);
      setPhase("grading");
      const result = await gradeAnswer({
        questionId: question.id,
        userName,
        userAnswer,
        currentScore: scoreboard.score,
      });
      setFeedback(`Score: ${result.score}/10\n${result.feedback}`);
      setScoreboard(result.scoreboard);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setPending(false);
    }
  };

  const resetGame = () => {
    setPhase("idle");
    setSelectedGroup(null);
    setUsedGroups([]);
    setQuestion(null);
    setUsedQuestions([]);
    setUserAnswer("");
    setUserName("");
    setFeedback(null);
    setScoreboard({
      score: 0,
      hasWinner: false,
      specialEvent: null,
    });
    setError(null);
  };

  const currentStatus = useMemo(() => {
    if (error) return error;
    if (pending) return "执行中...";
    if (phase === "idle") return "点击“抽取分组”开始游戏";
    if (phase === "group") return `当前分组: ${selectedGroup}`;
    if (phase === "question" && question) return "请阅读问题并填写答案";
    if (phase === "grading") return "AI 正在评分...";
    return "";
  }, [error, pending, phase, selectedGroup, question]);

  return (
    <div className="app-shell">
      <header>
        <div>
          <h1>Double Spin Wheel · Web</h1>
          <p>抽题、回答、让 OpenRouter AI 来评分 🎯</p>
        </div>
        <button className="ghost" onClick={resetGame}>
          重置游戏
        </button>
      </header>

      <main className="layout">
        <section className="panel status-panel">
          <h2>状态</h2>
          <p className="status">{currentStatus}</p>
          <div className="controls">
            <button onClick={handleSpinGroup} disabled={pending}>
              抽取分组
            </button>
            <button
              onClick={handleSpinQuestion}
              disabled={!selectedGroup || pending}
            >
              抽取问题
            </button>
          </div>
          <div className="scoreboard">
            <div>
              <span>当前积分</span>
              <strong>{scoreboard.score}</strong>
            </div>
            {scoreboard.specialEvent && (
              <p className="special">{scoreboard.specialEvent.message}</p>
            )}
            {scoreboard.hasWinner && (
              <p className="winner">🎉 已抵达 WIN 区域！</p>
            )}
          </div>
        </section>

        <section className="panel question-panel">
          <h2>
            {question
              ? `题目 · ${question.group}`
              : selectedGroup
                ? `等待抽题 · ${selectedGroup}`
                : "尚未抽取分组"}
          </h2>
          {question ? (
            <p className="question-text">{question.prompt}</p>
          ) : (
            <p className="placeholder">
              点击“抽取问题”获取一个随机问答。
            </p>
          )}

          <label className="input-block">
            <span>玩家名称</span>
            <input
              type="text"
              value={userName}
              placeholder="可选"
              onChange={(e) => setUserName(e.target.value)}
            />
          </label>

          <label className="input-block">
            <span>你的答案</span>
            <textarea
              rows={6}
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="输入你的想法..."
            />
          </label>

          <button
            className="primary"
            onClick={handleGrade}
            disabled={!question || pending}
          >
            提交并让 AI 评分
          </button>

          {feedback && (
            <pre className="feedback">
              {feedback}
            </pre>
          )}
        </section>

        <section className="panel sidebar">
          <h2>题库分组</h2>
          {loadingGroups ? (
            <p>加载中...</p>
          ) : (
            <ul>
              {groups.map((group) => (
                <li key={group.id}>
                  <span>{group.label}</span>
                  <span>{group.questionCount}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;

