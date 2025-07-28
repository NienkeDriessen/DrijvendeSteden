import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    // This allows Vite to accept requests from your public server address.
    allowedHosts: [
      'sciencecentreontour.tudelft.nl'
    ],
  },
});