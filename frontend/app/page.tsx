import Link from "next/link";

import { UploadForm } from "@/components/upload-form";
import { historyEnabled } from "@/lib/features";

export default function HomePage() {
  return (
    <div className="stack-xl">
      <section className="hero-card">
        <div className="hero-copy">
          <span className="eyebrow">Learning Focused MVP</span>
          <h1>把录音、PPT、PDF、讲义快速整理成真正能复习的资料</h1>
          <p>
            这个工具专注学习提效与考试复习。上传课堂材料后，会自动生成复习提纲、章节总结、高频考点、练习题和速记卡片，而不是泛泛摘要。
          </p>
        </div>
        <div className="hero-side">
          <div className="metric-card">
            <strong>5 类输出</strong>
            <span>提纲 / 总结 / 考点 / 题目 / 卡片</span>
          </div>
          <div className="metric-card alt">
            <strong>支持多格式</strong>
            <span>音频、PPTX、PDF、TXT、Markdown</span>
          </div>
          {historyEnabled ? (
            <Link href="/history" className="ghost-link">
              查看历史任务
            </Link>
          ) : null}
        </div>
      </section>

      <section className="panel-grid">
        <div className="panel wide">
          <div className="panel-heading">
            <h2>上传学习资料</h2>
            <p>支持多文件一起上传，后端会统一整理为结构化文本片段。</p>
          </div>
          <UploadForm />
        </div>

        <div className="panel">
          <div className="panel-heading">
            <h2>MVP 处理流程</h2>
          </div>
          <ol className="ordered-list">
            <li>上传课堂资料并创建任务</li>
            <li>后端解析为结构化片段并保留来源页码/段落</li>
            <li>生成考试风格的复习内容</li>
            <li>在结果页查看并导出 Markdown / PDF</li>
          </ol>
        </div>
      </section>
    </div>
  );
}