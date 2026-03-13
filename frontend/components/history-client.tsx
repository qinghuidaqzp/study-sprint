"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { fetchTasks } from "@/lib/api";
import type { TaskSummary } from "@/lib/types";
import { StatusBadge } from "@/components/status-badge";

export function HistoryClient() {
  const [tasks, setTasks] = useState<TaskSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    fetchTasks()
      .then((data) => {
        if (!active) return;
        setTasks(data);
      })
      .catch((fetchError) => {
        if (!active) return;
        setError(fetchError instanceof Error ? fetchError.message : "加载失败");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="stack-xl">
      <section className="section-header compact">
        <div>
          <h1>历史记录</h1>
          <p className="muted">按时间查看已上传的学习整理任务，可继续进入详情页查看结果和导出。</p>
        </div>
      </section>

      {loading ? <div className="panel">正在加载历史任务...</div> : null}
      {error ? <div className="error-box">{error}</div> : null}
      {!loading && !tasks.length ? <div className="empty-state">还没有任务，先去上传一份资料试试看。</div> : null}

      <div className="history-list">
        {tasks.map((task) => (
          <Link href={`/tasks/${task.id}`} key={task.id} className="history-card">
            <div className="section-header compact">
              <div>
                <strong>{task.title}</strong>
                <div className="task-meta">
                  {task.file_count} 个文件 · {task.segment_count} 个片段 · {task.output_count} 份输出
                </div>
              </div>
              <StatusBadge status={task.status} />
            </div>
            <div className="meta-row muted">
              <span>{new Date(task.created_at).toLocaleString("zh-CN")}</span>
              <span>{task.source_types.join(" / ") || "未识别类型"}</span>
            </div>
            {task.error_message ? <div className="error-box">{task.error_message}</div> : null}
          </Link>
        ))}
      </div>
    </div>
  );
}
