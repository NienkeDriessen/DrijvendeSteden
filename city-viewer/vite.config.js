import { defineConfig } from 'vite';
// fs is no longer needed

export default defineConfig({
  server: {
    // HTTPS configuration removed
    allowedHosts: [
      'sciencecentreontour.tudelft.nl'
    ],
  },
});