# HTTPS Deployment Guide

This document shows how to serve both the Flask recognition API and 3js
viewer securely on `https://sciencecentreontour.tudelft.nl` with automatic HTTP
→ HTTPS redirects. we use (https://caddyserver.com),
which terminates TLS and proxies requests to the existing Windows services.

## 1. Prerequisites

| Component | Purpose |
|-----------|---------|
| Python virtualenv + Flask service | Keeps `gateway.py` running on `http://127.0.0.1:5050` |
| Node/npm | Builds the viewer into static assets (`npm run build`) |
| Caddy (Windows build) | Handles TLS, HTTPS redirects, and reverse proxy routing |

Open inbound ports **80**, **443**, and **5050** on the Windows host and any upstream
firewalls. Port 80 is required for ACME/Let's Encrypt challenges, port 443 serves the
viewer, and port 5050 exposes the recognition UI behind TLS.

## 2. Prepare the applications

### 2.1 Flask recognition service

The service can keep running on HTTP internally. Make sure the following
environment variables are defined for the service (through NSSM, the service
wrapper, or PowerShell before launching `gateway.py`):

| Variable | Example | Purpose |
|----------|---------|---------|
| `VIEWER_BASE_URL` | `https://sciencecentreontour.tudelft.nl` | Used for QR-code links |
| `FRONTEND_ORIGIN` | `https://sciencecentreontour.tudelft.nl` | Tightens CORS to the viewer origin |
| `PREFERRED_URL_SCHEME` | `https` | Ensures `url_for(..., _external=True)` emits HTTPS URLs |

Restart the Flask service so the new settings take effect.

### 2.2 Viewer build

Deploy the static viewer bundle once:

```powershell
cd C:\Rec\UniStuff\SCD\floating_cities\DrijvendeSteden\city-viewer
npm install
npm run build
```

The build output lives in `city-viewer/dist/` and will be served directly by
Caddy. Whenever you update the viewer, run `npm run build` again.

## 3. Install and configure Caddy

1. **Download** the Windows build of Caddy from <https://caddyserver.com/download>.
2. **Extract** `caddy.exe` to a directory, e.g. `C:\Caddy`.
3. Copy `deployment/Caddyfile.example` from this repository to the same
   directory and rename it to `Caddyfile` (no extension). Verify paths inside
   the file match your workstation.

The provided configuration:

- Obtains/renews Let's Encrypt certificates automatically.
- Serves the static viewer from `city-viewer/dist/`.
- Proxies `/api/*`, `/link/*`, `/static/*`, and `/upload/*` to the Flask backend
  on `127.0.0.1:5050`.
- Terminates TLS on `https://sciencecentreontour.tudelft.nl:5050` and forwards the
   recognition UI to the Flask app, while redirecting `http://sciencecentreontour.tudelft.nl:5050`
   to the HTTPS version.
- Adds HSTS and other basic security headers.
- Redirects all HTTP traffic (port 80) to HTTPS automatically (Caddy default).

## 4. Run Caddy as a Windows service

Open **PowerShell as Administrator** and run:

```powershell
cd C:\Caddy
.\caddy.exe install
Start-Service caddy
```

This installs Caddy as `caddy` Windows service. Logs are stored in the Windows
Event Viewer by default. To test configuration changes without restarting the
service wrapper:

```powershell
.\caddy.exe reload
```

If you prefer to run Caddy in the foreground for debugging:

```powershell
.\caddy.exe run --config .\Caddyfile --watch
```

## 5. Verify

1. Browse to <http://sciencecentreontour.tudelft.nl>. You should be redirected
   to `https://` automatically.
2. Confirm browser security padlock appears and the certificate is issued by
   Let's Encrypt (or your chosen CA).
3. Test the API from a remote machine:

   ```powershell
   curl https://sciencecentreontour.tudelft.nl/api/viewer/ids
   ```

   4. Browse to <http://sciencecentreontour.tudelft.nl:5050> and verify it redirects to the
      HTTPS version on the same port. Then confirm the recognition UI loads at
      <https://sciencecentreontour.tudelft.nl:5050>.
   5. Upload a new city from the recognition UI and confirm the generated QR code
      now uses the HTTPS base URL.

## 6. Optional hardening

- Update the Flask `FRONTEND_ORIGIN` environment variable to a comma-separated
  list if additional allowed origins are required.
- Set up a scheduled task to rebuild the viewer bundle (if the project updates
  frequently).
- Configure Caddy access logs path and retention policy as needed.
- For non-public viewers, keep the API endpoints protected with Basic Auth and
  restrict access via additional Caddy `basicauth` blocks.

---

With these steps, both applications are served over HTTPS, and visitors landing
on the HTTP endpoint are redirected automatically. Caddy manages certificate
renewals, simplifying long-term maintenance.
