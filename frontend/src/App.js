import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { fetchGroups, gradeAnswer, spinGroup, spinQuestion, } from "./api";
import "./App.css";
function App() {
    const [groups, setGroups] = useState([]);
    const [loadingGroups, setLoadingGroups] = useState(false);
    const [phase, setPhase] = useState("idle");
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [usedGroups, setUsedGroups] = useState([]);
    const [question, setQuestion] = useState(null);
    const [usedQuestions, setUsedQuestions] = useState([]);
    const [userName, setUserName] = useState("");
    const [userAnswer, setUserAnswer] = useState("");
    const [scoreboard, setScoreboard] = useState({
        score: 0,
        hasWinner: false,
        specialEvent: null,
    });
    const [feedback, setFeedback] = useState(null);
    const [error, setError] = useState(null);
    const [pending, setPending] = useState(false);
    useEffect(() => {
        const load = async () => {
            setLoadingGroups(true);
            try {
                const data = await fetchGroups();
                setGroups(data);
            }
            catch (err) {
                setError(err.message);
            }
            finally {
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
            setUsedGroups((prev) => prev.includes(group) ? prev : [...prev, group]);
            setUsedQuestions([]);
        }
        catch (err) {
            setError(err.message);
        }
        finally {
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
        }
        catch (err) {
            setError(err.message);
        }
        finally {
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
        }
        catch (err) {
            setError(err.message);
        }
        finally {
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
        if (error)
            return error;
        if (pending)
            return "执行中...";
        if (phase === "idle")
            return "点击“抽取分组”开始游戏";
        if (phase === "group")
            return `当前分组: ${selectedGroup}`;
        if (phase === "question" && question)
            return "请阅读问题并填写答案";
        if (phase === "grading")
            return "AI 正在评分...";
        return "";
    }, [error, pending, phase, selectedGroup, question]);
    return (_jsxs("div", { className: "app-shell", children: [_jsxs("header", { children: [_jsxs("div", { children: [_jsx("h1", { children: "Double Spin Wheel \u00B7 Web" }), _jsx("p", { children: "\u62BD\u9898\u3001\u56DE\u7B54\u3001\u8BA9 OpenRouter AI \u6765\u8BC4\u5206 \uD83C\uDFAF" })] }), _jsx("button", { className: "ghost", onClick: resetGame, children: "\u91CD\u7F6E\u6E38\u620F" })] }), _jsxs("main", { className: "layout", children: [_jsxs("section", { className: "panel status-panel", children: [_jsx("h2", { children: "\u72B6\u6001" }), _jsx("p", { className: "status", children: currentStatus }), _jsxs("div", { className: "controls", children: [_jsx("button", { onClick: handleSpinGroup, disabled: pending, children: "\u62BD\u53D6\u5206\u7EC4" }), _jsx("button", { onClick: handleSpinQuestion, disabled: !selectedGroup || pending, children: "\u62BD\u53D6\u95EE\u9898" })] }), _jsxs("div", { className: "scoreboard", children: [_jsxs("div", { children: [_jsx("span", { children: "\u5F53\u524D\u79EF\u5206" }), _jsx("strong", { children: scoreboard.score })] }), scoreboard.specialEvent && (_jsx("p", { className: "special", children: scoreboard.specialEvent.message })), scoreboard.hasWinner && (_jsx("p", { className: "winner", children: "\uD83C\uDF89 \u5DF2\u62B5\u8FBE WIN \u533A\u57DF\uFF01" }))] })] }), _jsxs("section", { className: "panel question-panel", children: [_jsx("h2", { children: question
                                    ? `题目 · ${question.group}`
                                    : selectedGroup
                                        ? `等待抽题 · ${selectedGroup}`
                                        : "尚未抽取分组" }), question ? (_jsx("p", { className: "question-text", children: question.prompt })) : (_jsx("p", { className: "placeholder", children: "\u70B9\u51FB\u201C\u62BD\u53D6\u95EE\u9898\u201D\u83B7\u53D6\u4E00\u4E2A\u968F\u673A\u95EE\u7B54\u3002" })), _jsxs("label", { className: "input-block", children: [_jsx("span", { children: "\u73A9\u5BB6\u540D\u79F0" }), _jsx("input", { type: "text", value: userName, placeholder: "\u53EF\u9009", onChange: (e) => setUserName(e.target.value) })] }), _jsxs("label", { className: "input-block", children: [_jsx("span", { children: "\u4F60\u7684\u7B54\u6848" }), _jsx("textarea", { rows: 6, value: userAnswer, onChange: (e) => setUserAnswer(e.target.value), placeholder: "\u8F93\u5165\u4F60\u7684\u60F3\u6CD5..." })] }), _jsx("button", { className: "primary", onClick: handleGrade, disabled: !question || pending, children: "\u63D0\u4EA4\u5E76\u8BA9 AI \u8BC4\u5206" }), feedback && (_jsx("pre", { className: "feedback", children: feedback }))] }), _jsxs("section", { className: "panel sidebar", children: [_jsx("h2", { children: "\u9898\u5E93\u5206\u7EC4" }), loadingGroups ? (_jsx("p", { children: "\u52A0\u8F7D\u4E2D..." })) : (_jsx("ul", { children: groups.map((group) => (_jsxs("li", { children: [_jsx("span", { children: group.label }), _jsx("span", { children: group.questionCount })] }, group.id))) }))] })] })] }));
}
export default App;
