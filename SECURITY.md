# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@aiblog-generator.dev` with:

- A description of the issue and its impact.
- Steps to reproduce, or a minimal proof of concept.
- The affected version(s) and OS build.
- Whether you intend to disclose publicly and on what timeline.

We aim to acknowledge within 72 hours and to ship a fix or mitigation within
14 days for high-severity issues.

## Threat model notes

This is a local desktop tool. It stores API keys in the Windows Credential
Manager via `keyring`. It never phones home. The only outbound traffic is to
the LLM provider endpoints you configure. If you find code that sends user
content anywhere else, that is a critical bug — report it.

## API key handling

- Keys are read from `keyring`, never from plain files by default.
- `config.local.toml` may hold non-secret overrides only.
- Logs redact anything matching the `sk-*`, `anthropic-*`, and bearer-token
  patterns before writing.