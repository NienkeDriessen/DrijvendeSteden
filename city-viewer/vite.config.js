import { defineConfig } from 'vite';
import basicSsl from '@vitejs/plugin-basic-ssl';

export default defineConfig({
  plugins: [
    // This plugin will automatically generate and trust a self-signed certificate.
    basicSsl()
  ],
  server: {
    // The `https` option is no longer needed here, as the plugin handles it.
    // This allows Vite to accept requests from your public server address.
    allowedHosts: [
      'sciencecentreontour.tudelft.nl'
    ],
  },
});