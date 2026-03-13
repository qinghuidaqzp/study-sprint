import type { ContentSegmentRead } from "@/lib/types";

export function SegmentsPreview({ segments }: { segments: ContentSegmentRead[] }) {
  if (!segments.length) {
    return <div className="empty-state">解析完成后，这里会显示原始文本片段概览。</div>;
  }

  return (
    <section className="result-panel">
      <div className="section-header compact">
        <div>
          <h2>原始解析文本概览</h2>
          <p className="muted">预览前 12 个片段，保留来源标签，方便核对生成内容是否贴合原文。</p>
        </div>
      </div>
      <div className="segment-list">
        {segments.map((segment) => (
          <article key={segment.id} className="segment-card">
            <strong>{segment.source_label}</strong>
            <div className="status-line">片段 #{segment.segment_order}</div>
            <p>{segment.content}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
