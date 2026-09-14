# Privacy

SnapShield is local-first. User content enters through an explicit browser action and is processed by a service bound to localhost. There is no cloud model, telemetry client, URL fetch, or silent network fallback.

Raw messages and images are not persisted. The incident store keeps a SHA-256 input hash, time, type, score, severity, category, indicator count, processing time, provider, model version, and sanitized signal names. Hashes may still permit guessing of common messages and should be protected as local application data.

Logs contain startup state, selected provider, HTTP route/status metadata, errors, and benchmark events. Application code does not log submitted content. Development servers may log route paths but request bodies are excluded.

The UI displays redacted sensitive data by default. Original input remains in the current browser component state so the user can edit it; close the app or replace the text to remove it from that session. Clearing history deletes all SQLite incident rows but cannot securely erase storage sectors.

