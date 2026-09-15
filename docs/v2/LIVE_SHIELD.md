# Live Shield

Live Shield is an opt-in Windows text-clipboard monitor. It is off at every process start and requires explicit consent through the API/UI. It does not install keystroke hooks, read browser history, record the screen, navigate URLs, or transmit content to a cloud service.

While enabled it considers only new supported text changes up to 50,000 characters, deduplicates the last 128 content hashes, and rate-limits analysis to one item per three seconds. Alerts are nonblocking, expire after one minute, and are volatile. Disabling clears the active alert and deduplication state; an in-flight analysis result is discarded. No incident is persisted unless the user explicitly selects **Save sanitized incident**.

Tests prove off-by-default behavior, explicit-consent enforcement, rate limiting, deduplication, volatile alerts and no implicit persistence. Windows clipboard availability is reported truthfully; manual analysis remains available after any adapter error.
