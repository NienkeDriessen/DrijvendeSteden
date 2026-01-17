# DrijvendeSteden (city-recognition)

## Server-side input validation

All incoming data is treated as untrusted.

### Required environment variables

- `RECOG_SECRET_KEY`: required for Flask sessions/flash messages.
	- Set `RECOG_ALLOW_INSECURE_SECRET_KEY=1` only for local dev if you really need to bypass the startup check.

### Upload constraints

- Request size limit: 20 MB
- Allowed upload mimetypes: PNG/JPEG/WebP
- Max image pixels: 30,000,000

### City name constraints

- Max length: 100 characters
- Allowed characters: letters, numbers, spaces, `_`, `-`, `'`