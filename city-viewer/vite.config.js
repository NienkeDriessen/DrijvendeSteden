import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    // Enable HTTPS. Vite will automatically generate a self-signed certificate.
    https: true,
    // This allows Vite to accept requests from your public server address.
    // Note: It's better to be specific with hostnames than allowing all.
    allowedHosts: [
      'sciencecentreontour.tudelft.nl'
    ],
  },
});