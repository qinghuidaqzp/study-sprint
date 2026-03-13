import type { TaskCreateResponse, TaskDetail, TaskSummary } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = "请求失败";
    try {
      const data = await response.json();
      message = data.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export async function createTask(formData: FormData): Promise<TaskCreateResponse> {
  const response = await fetch(`${API_BASE}/api/tasks`, {
    method: "POST",
    body: formData,
  });
  return handleResponse<TaskCreateResponse>(response);
}

export async function fetchTask(taskId: string): Promise<TaskDetail> {
  const response = await fetch(`${API_BASE}/api/tasks/${taskId}`, {
    cache: "no-store",
  });
  return handleResponse<TaskDetail>(response);
}

export async function fetchTasks(): Promise<TaskSummary[]> {
  const response = await fetch(`${API_BASE}/api/tasks`, {
    cache: "no-store",
  });
  return handleResponse<TaskSummary[]>(response);
}

export function getExportUrl(taskId: string, format: "markdown" | "pdf"): string {
  return `${API_BASE}/api/tasks/${taskId}/export/${format}`;
}
