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
- Default placeholder: `https://your-app-domain.vercel.app`

## Before building APK

You need a live public frontend URL, for example:

```text
https://your-app-domain.vercel.app
```

Then run in `frontend`:

```powershell
$env:CAPACITOR_SERVER_URL="https://your-app-domain.vercel.app"
npm run cap:add:android
npm run cap:sync
```

## To build the APK

You need Android Studio or Android command line SDK installed.

Then either:

1. Open Android Studio:

```powershell
npm run android:open
```

Build menu:

- `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`

2. Or use Gradle in the generated Android project:

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
- Gradle reached the Android dependency resolution stage.

## Current local blocker

On this machine, APK compilation is currently blocked by Gradle failing to download Android and Maven artifacts over TLS/network.

That means:

- the mobile wrapper setup is already in place
- the remaining problem is environment/network related, not application code related

## Notes

- The APK will only work correctly when `CAPACITOR_SERVER_URL` points to a reachable public site.
- For phone testing, deploying the frontend first is required.
- If you later switch domains, update `CAPACITOR_SERVER_URL` and run `npm run cap:sync` again.
- This wrapper approach is the fastest way to get an installable Android package without rewriting the app in React Native or Flutter.