# Pluang read-only trial

The Pluang MCP shown as enabled in ChatGPT is not automatically accessible from the QuantSyariah backend. No authenticated live Pluang API access is claimed.

Run the offline import after the user exports a JSON portfolio snapshot:

```bash
python -m backend.pluang_trial /path/to/snapshot.json
```

Input must satisfy `backend.pluang_snapshot.normalize_snapshot`. The report contains symbol count, ticker list, and total value, and explicitly sets `account_connected=false`, `live_orders_enabled=false`, and `sharia_status=unverified`. Do not commit portfolio exports or secrets. APK build remains deferred.
