"use client";

import { useEffect, useState } from "react";

import { fetchTask, getExportUrl } from "@/lib/api";
import type { TaskDetail } from "@/lib/types";
import { ResultTabs } from "@/components/result-tabs";
import { SegmentsPreview } from "@/components/segments-preview";
import { StatusBadge } from "@/components/status-badge";

const pollingStatuses = new Set(["uploaded", "parsing", "generating"]);

export function TaskDetailClient({ taskId }: { taskId: string }) {
  const [task, setTask] = useState<TaskDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    let timer: ReturnType<typeof setTimeout> | undefined;

    async function loadTask() {
      try {
        const data = await fetchTask(taskId);
        if (!active) return;
        setTask(data);
        setError(null);
        if (pollingStatuses.has(data.status)) {
          timer = setTimeout(loadTask, 3000);
        }
      } catch (fetchError) {
        if (!active) return;
        setError(fetchError instanceof Error ? fetchError.message : "加载任务失败");
      } finally {
        if (active) setLoading(false);
      }
    }

    void loadTask();
    return () => {
      active = false;
      if (timer) clearTimeout(timer);
    };
  }, [taskId]);

  if (loading) {
    return <div className="panel">正在加载任务详情...</div>;
  }

  if (error) {
    return <div className="error-box">{error}</div>;
  }

  if (!task) {
    return <div className="empty-state">任务不存在或已被删除。</div>;
  }

  return (
    <div className="stack-xl">
      <section className="section-header">
        <div>
          <h1>{task.title}</h1>
          <p className="muted">处理状态会自动轮询更新，完成后即可复制与导出。</p>
        </div>
        <div className="status-group">
          <StatusBadge status={task.status} />
          <a className="secondary-button" href={getExportUrl(task.id, "markdown")}>
            导出 Markdown
          </a>
          <a className="secondary-button" href={getExportUrl(task.id, "pdf")}>
            导出 PDF
          </a>
        </div>
      </section>

      {task.status !== "completed" ? (
        <div className="info-card">
          <strong>当前进度</strong>
          <div className="muted">
            {task.status === "uploaded" && "文件已上传，正在排队处理。"}
            {task.status === "parsing" && "后端正在解析文件内容并整理文本片段。"}
            {task.status === "generating" && "后端正在生成复习提纲、考点、题目和卡片。"}
            {task.status === "failed" && "任务处理失败，请检查错误信息后重新上传或调整配置。"}
          </div>
          {task.error_message ? <div className="error-box">{task.error_message}</div> : null}
        </div>
      ) : null}

      <section className="info-grid">
        <div className="info-card">
          <div className="section-header compact">
            <div>
              <h2>文件信息</h2>
            </div>
          </div>
          <div className="file-list">
            {task.files.map((file) => (
              <article key={file.id} className="file-item">
                <strong>{file.original_name}</strong>
                <div className="file-meta">
                  类型：{file.file_type} · 大小：{(file.size_bytes / 1024).toFixed(1)} KB
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="info-card">
          <div className="section-header compact">
            <div>
              <h2>任务概览</h2>
            </div>
          </div>
          <div className="stack-sm">
            <div className="inline-note">来源类型：{task.source_types.join(" / ") || "未识别"}</div>
            <div className="inline-note">解析片段：{task.segment_count}</div>
            <div className="inline-note">生成模块：{task.output_count}</div>
            <div className="muted">创建时间：{new Date(task.created_at).toLocaleString("zh-CN")}</div>
          </div>
        </div>
      </section>

      <SegmentsPreview segments={task.segments_preview} />
      <ResultTabs task={task} />
    </div>
  );
}

