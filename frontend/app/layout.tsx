import "./globals.css";
import type { ReactNode } from "react";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "学习资料整理与复习生成器",
  description: "上传课堂资料，自动生成复习提纲、章节总结、考点、练习题与速记卡片。",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <div className="app-shell">
          <header className="topbar">
            <Link href="/" className="brand">
              Study Sprint
            </Link>
            <nav className="nav-links">
              <Link href="/">上传页</Link>
              <Link href="/history">历史记录</Link>
            </nav>
          </header>
          <main className="page-wrap">{children}</main>
        </div>
      </body>
    </html>
  );
}
