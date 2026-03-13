"use client";

import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useRouter } from "next/navigation";

import { createTask } from "@/lib/api";

const acceptedTypes = ".pdf,.pptx,.txt,.md,.mp3,.wav,.m4a";

export function UploadForm() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const helperText = useMemo(() => {
    if (!files.length) {
      return "支持上传多份课堂资料，建议使用课程名 + 日期作为标题。";
    }
    return `已选择 ${files.length} 个文件，提交后会自动开始解析和生成。`;
  }, [files]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!title.trim()) {
      setError("请先填写任务标题，例如：高等数学期末复习。");
      return;
    }
    if (!files.length) {
      setError("请至少选择一个文件后再提交。");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("title", title.trim());
      files.forEach((file) => formData.append("files", file));
      const task = await createTask(formData);
      router.push(`/tasks/${task.id}`);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "提交失败，请稍后重试。");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <div className="field-group">
        <label htmlFor="task-title">任务标题</label>
        <input
          id="task-title"
          className="text-input"
          placeholder="例如：管理学期末冲刺复习"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>

      <div className="field-group">
        <label htmlFor="task-files">上传文件</label>
        <div className="drop-hint">
          <input
            id="task-files"
            className="file-input"
            type="file"
            accept={acceptedTypes}
            multiple
            onChange={(event) => setFiles(Array.from(event.target.files ?? []))}
          />
          <p className="muted">支持格式：PDF / PPTX / TXT / Markdown / MP3 / WAV / M4A</p>
        </div>
      </div>

      {files.length > 0 ? (
        <div className="file-chip-wrap">
          {files.map((file) => (
            <span key={`${file.name}-${file.size}`} className="file-chip">
              {file.name}
            </span>
          ))}
        </div>
      ) : null}

      <div className="inline-note">{helperText}</div>

      {error ? <div className="error-box">{error}</div> : null}

      <div className="action-row">
        <button type="submit" className="primary-button" disabled={submitting}>
          {submitting ? "正在创建任务..." : "开始生成复习资料"}
        </button>
      </div>
    </form>
  );
}
