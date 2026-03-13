import type { TaskStatus } from "@/lib/types";

const labels: Record<TaskStatus, string> = {
  uploaded: "已上传",
  parsing: "解析中",
  generating: "生成中",
  completed: "已完成",
  failed: "失败",
};

export function StatusBadge({ status }: { status: TaskStatus }) {
  return <span className={`status-badge status-${status}`}>{labels[status]}</span>;
}
