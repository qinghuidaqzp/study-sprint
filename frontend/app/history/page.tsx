import { notFound } from "next/navigation";

import { HistoryClient } from "@/components/history-client";
import { historyEnabled } from "@/lib/features";

export default function HistoryPage() {
  if (!historyEnabled) {
    notFound();
  }
  return <HistoryClient />;
}