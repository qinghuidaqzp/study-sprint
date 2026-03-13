# APK Guide

This project can be packaged as an Android APK by wrapping the deployed frontend in a Capacitor Android shell.

## How this works

- The real app still runs as a web app.
- The Android APK is a native shell that opens your deployed frontend URL.
- The backend remains deployed separately.

## Current setup

Capacitor config file:

- `frontend/capacitor.config.ts`

Android project:

- `frontend/android`

Important behavior:

- `CAPACITOR_SERVER_URL` controls which deployed URL the APK loads.
- Default URL in the repo is now `https://study-sprint-1lbk.vercel.app`.
- You can override that URL in GitHub Actions or local builds.

## GitHub Actions APK build

This repo now includes an Android APK workflow:

- `.github/workflows/build-android-apk.yml`

What it does:

- installs Node.js and Java on the GitHub runner
- installs Android SDK packages for API 36
- runs `npx cap sync android`
- builds `app-debug.apk`
- uploads the APK as a GitHub Actions artifact

How to use it on GitHub:

1. Open the repository `Actions` tab.
2. Choose `Build Android APK`.
3. Click `Run workflow`.
4. Optional: enter a different `server_url` if the APK should load another frontend domain.
5. Wait for the run to finish.
6. Download the artifact named `study-sprint-debug-apk`.

Optional repository variable:

- Name: `CAPACITOR_SERVER_URL`
- Example: `https://study-sprint-1lbk.vercel.app`

If you do not set that variable, the workflow falls back to the current deployed frontend URL.

## Local build option

You can still build locally if your machine has Android Studio or command line SDK tools installed.

Run in `frontend`:

```powershell
$env:CAPACITOR_SERVER_URL="https://study-sprint-1lbk.vercel.app"
npm run cap:sync
```

Then either open Android Studio:

```powershell
npm run android:open
```

Or use Gradle directly:

```powershell
cd android
$env:JAVA_HOME="D:\develop\Java\jdk-21"
.\gradlew assembleDebug
```

Expected APK output:

```text
frontend/android/app/build/outputs/apk/debug/app-debug.apk
```

## What I verified locally

- Capacitor packages installed successfully.
- `frontend/android` was generated successfully.
- `npm run cap:sync` completed successfully.
- The Android shell now points to the deployed frontend by default.

## Known limitation

On this machine, local APK compilation previously failed during Gradle dependency download because of network/TLS issues.

That is why GitHub Actions is the preferred build path now.

## Notes

- The generated artifact is a debug APK, which is the fastest installable format for MVP testing.
- If you later change the frontend domain, update `CAPACITOR_SERVER_URL` and rerun the workflow.
- This wrapper approach is the fastest way to get an installable Android package without rewriting the app in React Native or Flutter.