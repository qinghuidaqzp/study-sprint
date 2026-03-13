export type TaskStatus = "uploaded" | "parsing" | "generating" | "completed" | "failed";
export type OutputType = "outline" | "chapter_summary" | "key_points" | "quiz" | "flashcards";

export interface TaskSummary {
  id: string;
  title: string;
  status: TaskStatus;
  source_types: string[];
  error_message?: string | null;
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
  file_count: number;
  segment_count: number;
  output_count: number;
}

export interface SourceFileRead {
  id: string;
  original_name: string;
  stored_name: string;
  file_type: string;
  mime_type: string;
  size_bytes: number;
  storage_path: string;
  created_at: string;
}

export interface ContentSegmentRead {
  id: string;
  source_type: string;
  source_label: string;
  segment_order: number;
  content: string;
  metadata_json: Record<string, unknown>;
  created_at: string;
}

export interface GeneratedOutputRead {
  id: string;
  output_type: OutputType;
  title: string;
  content_markdown: string;
  content_json?: Record<string, unknown> | unknown[] | null;
  created_at: string;
}

export interface TaskDetail extends TaskSummary {
  files: SourceFileRead[];
  segments_preview: ContentSegmentRead[];
  outputs: Partial<Record<OutputType, GeneratedOutputRead>>;
}

export interface TaskCreateResponse {
  id: string;
  title: string;
  status: TaskStatus;
  message: string;
}

export const outputLabels: Record<OutputType, string> = {
  outline: "复习提纲",
  chapter_summary: "章节总结",
  key_points: "高频考点",
  quiz: "练习题",
  flashcards: "速记卡片",
};
