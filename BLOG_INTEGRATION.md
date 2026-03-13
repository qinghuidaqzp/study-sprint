# Blog Integration Guide

If your blog is a static site connected to a GitHub repository, do not try to run this full app inside the blog repo.

This MVP needs:

- a Next.js frontend
- a FastAPI backend
- a database
- file upload storage

A static blog can host an entry page, but not the full runtime stack.

## Recommended architecture

Use this split:

1. Keep the app as its own deployable project.
2. Deploy the app frontend to Vercel.
3. Deploy the backend and database to Render.
4. Add a blog page that links to the app or embeds it with an iframe.

## Option A: link from your blog

This is the safest approach.

Markdown snippet:

```md
## Study Sprint

I built a study-material organizer for revision use cases.

- Supports PDF, PPTX, TXT, and Markdown uploads
- Generates outlines, chapter summaries, key points, quizzes, and flashcards

[Open the app](https://your-app-domain.vercel.app)
```

## Option B: embed in your blog with iframe

Use this only if your blog platform allows raw HTML.

```html
<section>
  <h2>Study Sprint</h2>
  <p>Upload course material and generate revision notes, key points, quizzes, and flashcards.</p>
  <p><a href="https://your-app-domain.vercel.app" target="_blank" rel="noreferrer">Open in full page</a></p>
  <iframe
    src="https://your-app-domain.vercel.app"
    title="Study Sprint"
    loading="lazy"
    style="width: 100%; min-height: 900px; border: 1px solid #ddd; border-radius: 12px; background: #fff;"
  ></iframe>
</section>
```

## Platform notes

### GitHub Pages / Jekyll / Hexo / Hugo

These are typically static.

Use:

- a link page, or
- an iframe embed page

Do not try to run the FastAPI backend inside the blog repo.

### Vercel-hosted blog

If your blog itself is already on Vercel, you can still keep this app as a separate project under the same GitHub account and link to it from the blog.

## What to deploy first

1. Deploy the backend and database.
2. Deploy the frontend with `NEXT_PUBLIC_API_BASE_URL` pointing to the backend.
3. Add the app URL to your blog post or page.

## Mobile recommendation

For phone use, the cleanest setup is:

- blog post introduces the tool
- one button opens the app in a new tab

That is usually better than embedding the full app in a narrow blog layout.