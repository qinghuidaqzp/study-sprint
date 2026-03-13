"use client";

import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { outputLabels, type OutputType, type TaskDetail } from "@/lib/types";

const outputOrder: OutputType[] = ["outline", "chapter_summary", "key_points", "quiz", "flashcards"];

export function ResultTabs({ task }: { task: TaskDetail }) {
  const availableTabs = useMemo(
    () => outputOrder.filter((type) => task.outputs[type]?.content_markdown),
    [task.outputs],
  );
  const [activeTab, setActiveTab] = useState<OutputType>(availableTabs[0] ?? "outline");

  useEffect(() => {
    if (!availableTabs.length) return;
    if (!availableTabs.includes(activeTab)) {
      setActiveTab(availableTabs[0]);
    }
  }, [activeTab, availableTabs]);

  const activeOutput = task.outputs[activeTab];

  async function copyCurrentOutput() {
    if (!activeOutput?.content_markdown) return;
    await navigator.clipboard.writeText(activeOutput.content_markdown);
  }

  return (
    <section className="tab-panel">
      <div className="section-header compact">
        <div>
          <h2>学习资料生成结果</h2>
          <p className="muted">按模块切换查看，内容偏向考前复习而不是普通摘要。</p>
        </div>
        <div className="result-actions">
          <button type="button" className="inline-button small" onClick={copyCurrentOutput} disabled={!activeOutput}>
            复制当前模块
          </button>
        </div>
      </div>

      <div className="tab-list">
        {outputOrder.map((type) => (
          <button
            key={type}
            type="button"
            className={`tab-button ${activeTab === type ? "active" : ""}`}
            onClick={() => setActiveTab(type)}
          >
            {outputLabels[type]}
          </button>
        ))}
      </div>

      {activeOutput ? (
        <div className="markdown">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{activeOutput.content_markdown}</ReactMarkdown>
        </div>
      ) : (
        <div className="empty-state">当前模块还没有生成完成。</div>
      )}
    </section>
  );
}
