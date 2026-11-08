"""Production safety note: Pluang default, real orders disabled.

The old /pluang/order/draft accepted user-supplied sharia_verified and
market_data_verified booleans. That endpoint must return HTTP 410.

Use /trade/preview only for non-executing previews with operator-reviewed
screening evidence, a timestamped quote and portfolio information. These
inputs are still untrusted if supplied by clients, and MUST NOT be used
to authorize real orders. OAuth Pluang, licensed feeds, OJK verification
and US broker sessions are not connected.

The Pluang MCP configuration in ChatGPT does not automatically authorize
an external Android app to read a user's Pluang account.
