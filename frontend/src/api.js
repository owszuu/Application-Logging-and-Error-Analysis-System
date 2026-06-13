export const API_URL = "http://localhost:9000";

export async function fetchJSON(path) {
    const res = await fetch(`${API_URL}${path}`);
    if (!res.ok) throw new Error("API error: " + res.status);
    return res.json();
}
