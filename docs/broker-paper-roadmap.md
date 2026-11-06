# QuantSyariah broker adapter plan

- Alpaca: only `https://paper-api.alpaca.markets` may be used for paper-order API calls. Never fall back to live host. API keys must be stored server-side and must not be committed.
- IBKR: paper account must be selected in TWS/IB Gateway; verify paper account identity before any paper order. No live-order adapter until separately approved.
- All markets: deny trades without independently verified Sharia eligibility, fresh licensed market data, configured limits, and kill switch.
- Pluang: assisted orders only, requiring user confirmation.
- Simulator and broker paper accounts are distinct; simulated fills are not broker-confirmed executions.

Official references: https://docs.alpaca.markets/ and https://www.interactivebrokers.com/docs/.
