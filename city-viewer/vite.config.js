import { defineConfig } from 'vite';
import fs from 'fs';

export default defineConfig({
  // Remove the basic-ssl plugin if it's there
  server: {
    https: {
      // Adjust paths if you run vite from a different directory
      key: fs.readFileSync('../cert.key'),
      cert: fs.readFileSync('../cert.crt'),
    },
    allowedHosts: [
      'sciencecentreontour.tudelft.nl'
    ],
  },
});