# Pluang snapshot validation API (read-only)

POST /pluang/snapshot/validate requires Authorization: Bearer <QUANT_GATEWAY_TOKEN>.
It accepts only user-exported IDR snapshots of IDX equity tickers, checks timezone,
freshness, duplicates, and finite nonnegative amounts. It returns an explicitly
non-live, non-tradable normalized snapshot; it does not store portfolio data.

This endpoint does NOT connect to Pluang MCP or authorize access to an account.
Pluang OAuth in ChatGPT is independent of the QuantSyariah Android app.
Do not submit passwords, OTP, OAuth access tokens, or other credentials as snapshot data.
Official OJK Sharia verification remains a separate mandatory step.
