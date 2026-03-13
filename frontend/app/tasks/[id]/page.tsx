import { TaskDetailClient } from "@/components/task-detail-client";

export default function TaskDetailPage({ params }: { params: { id: string } }) {
  return <TaskDetailClient taskId={params.id} />;
}
