import type { CapacitorConfig } from '@capacitor/cli';

const serverUrl = process.env.CAPACITOR_SERVER_URL || 'https://study-sprint-1lbk.vercel.app';

const config: CapacitorConfig = {
  appId: 'com.dasan.studysprint',
  appName: 'Study Sprint',
  webDir: 'capacitor-shell',
  server: {
    url: serverUrl,
    cleartext: serverUrl.startsWith('http://'),
    androidScheme: serverUrl.startsWith('http://') ? 'http' : 'https',
  },
};

export default config;