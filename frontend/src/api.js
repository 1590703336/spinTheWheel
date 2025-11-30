const API_BASE = import.meta.env.VITE_API_BASE || "";
async function request(path, init) {
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
export async function fetchGroups() {
    const data = await request("/api/groups");
    return data.groups;
}
export async function spinGroup(exclude) {
    const data = await request("/api/spin-group", {
        method: "POST",
        body: JSON.stringify({ excludeGroups: exclude }),
    });
    return data.group;
}
export async function spinQuestion(group, excludeQuestionIds) {
    return request("/api/spin-question", {
        method: "POST",
        body: JSON.stringify({ group, excludeQuestionIds }),
    });
}
export async function gradeAnswer(params) {
    return request("/api/grade-answer", {
        method: "POST",
        body: JSON.stringify(params),
    });
}
