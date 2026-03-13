# Deployment Guide

This project cannot run on GitHub Pages or a static blog by itself because it needs:

- a Next.js frontend
- a FastAPI backend
- a relational database
- uploaded file handling

The shortest public deployment path is:

- GitHub for source control
- Vercel for `frontend`
- Render for `backend` and PostgreSQL

## 1. Push to GitHub

Initialize the repository locally:

```powershell
cd E:\Dasan\appthird
git init -b main
git add .
git commit -m "Initial Study Sprint MVP"
```

Create an empty GitHub repository in the browser, then connect and push:

```powershell
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 2. Deploy the backend on Render

This repo includes `render.yaml`, so you can use Render Blueprints.

Steps:

1. Open the Render dashboard.
2. Choose `New +` -> `Blueprint`.
3. Connect your GitHub account and select this repository.
4. Render will detect `render.yaml` in the repository root.
5. When prompted, set `CORS_ORIGINS` to your frontend domain, for example:

```text
["https://your-frontend.vercel.app"]
```

After deployment, copy the backend URL, for example:

```text
https://study-sprint-api.onrender.com
```

Important notes:

- The current `render.yaml` is configured for the Render free plan.
- Free Render web services do not provide a persistent disk, so `STORAGE_ROOT` is set to `/tmp/study-sprint`.
- Uploaded files and generated exports on the backend are therefore ephemeral in this free setup.
- Audio transcription is not enabled in the default free deployment path. `WHISPER_BACKEND` is set to `openai`, which means audio needs a compatible remote API key before it will work online.
- The backend is pinned to Python `3.11.11` because that is the version validated locally.

## 3. Deploy the frontend on Vercel

Steps:

1. Open the Vercel dashboard.
2. Import the same GitHub repository.
3. Set the project `Root Directory` to:

```text
frontend
```

4. Add this environment variable in Vercel:

```text
NEXT_PUBLIC_API_BASE_URL=https://study-sprint-api.onrender.com
```

Replace the value with your actual Render backend URL.

5. Deploy.

Vercel will build the Next.js app from the `frontend` directory.

## 4. Set the APK shell target URL

Once the frontend is live, set the APK shell URL to your deployed frontend domain:

```text
CAPACITOR_SERVER_URL=https://your-frontend.vercel.app
```

That value is used by `frontend/capacitor.config.ts` when you sync or build the Android shell.

## 5. Test from your phone

Once both deployments are live:

- open the Vercel URL on your phone
- upload a `txt`, `md`, `pdf`, or `pptx`
- wait for the task status to become `completed`
- open exports and generated study outputs

## 6. Current deployment limitations

- The simplest cloud path currently focuses on `txt`, `md`, `pdf`, and `pptx`.
- Audio uploads require extra configuration because the online deployment does not install local Whisper dependencies by default.
- Generated content uses `mock` mode by default. If you want real model output, configure `AI_PROVIDER`, `AI_BASE_URL`, `AI_API_KEY`, and `AI_MODEL` on the backend.
- Render free services can sleep when idle, so the first request after inactivity may be slow.
- Free-tier backend file storage is temporary. If you need persistent uploads and exports, move storage to S3-compatible object storage or switch the backend to a paid plan with persistent storage.

## 7. Recommended production env vars

Backend on Render:

```text
APP_ENV=production
AI_PROVIDER=mock
WHISPER_BACKEND=openai
STORAGE_ROOT=/tmp/study-sprint
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

Frontend on Vercel:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com
```
