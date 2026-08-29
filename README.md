# WeatherAI API Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![pytest](https://img.shields.io/badge/pytest-8.0%2B-brightgreen.svg)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-Automated-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A production-grade, enterprise-ready API Test Automation Framework designed for the **WeatherAI Developer Platform** (`https://api.weather-ai.co`). Built by a Senior QA Automation Engineer, this framework validates API contract compliance, functional requirements, edge-case boundaries, authentication/authorization security, response performance, and quota management.

---

## 1. Overview

The **WeatherAI API Test Automation Framework** provides comprehensive test coverage across WeatherAI REST endpoints (`/v1/weather`, `/v1/current`, `/v1/forecast`, `/v1/daily`, `/v1/hourly`, `/v1/weather-geo`, `/v1/ip-lookup`, `/v1/usage`, and `/v1/webhooks`).

### QA Risks Addressed:
1. **Contract Drift & Schema Regressions**: Detects unexpected breaking changes in response JSON structure or key data types before production deployment.
2. **Security & Authentication Leaks**: Prevents unauthorized API access and ensures API keys/Bearer tokens are never printed to console logs, test artifacts, or CI outputs.
3. **Input Boundary Vulnerabilities**: Prevents unhandled server exceptions (HTTP 500) when out-of-range coordinates, invalid day counts, or malformed parameters are submitted.
4. **Performance Degradation**: Monitors request latency and p95 thresholds under non-destructive conditions.
5. **Quota & Rate-Limit Exhaustion**: Validates rate-limiting headers without consuming client monthly quota.

---

## 2. Tech Stack

- **Core Language**: Python 3.12+
- **Test Runner & Framework**: `pytest` 8.0+
- **HTTP Client**: `requests` 2.31+
- **Schema Validation**: `jsonschema` 4.20+
- **Environment Management**: `python-dotenv` 1.0+ & `pydantic` 2.0+
- **Reporting**: `pytest-html` 4.1+ (Self-contained HTML reports)
- **Mocking & Offline Adapter**: `requests-mock` 1.11+
- **CI/CD Automation**: GitHub Actions

---

## 3. Test Strategy & Architecture

The framework enforces a clean, decoupled 7-layer architectural pattern:

```
weatherai-api-tests/
│
├── .github/
│   └── workflows/
│       └── api-tests.yml        # CI/CD Pipeline workflow
│
├── clients/
│   └── weather_api_client.py   # Centralized HTTP client encapsulating requests & auth
│
├── config/
│   ├── settings.py             # Environment configuration & secret loading
│   └── test_data.py            # Centralized parameter datasets & boundary matrices
│
├── schemas/                    # JSON Schema definition files
│   ├── weather_schema.json
│   ├── usage_schema.json
│   ├── error_schema.json
│   ├── ip_lookup_schema.json
│   └── webhook_schema.json
│
├── utils/
│   ├── assertions.py           # Reusable domain-specific assertion helpers
│   ├── helpers.py              # Schema loaders & utility functions
│   ├── logger.py               # Secret-sanitizing logger formatter
│   └── mock_responses.py       # Contract-compliant offline/CI mock data provider
│
├── tests/
│   ├── conftest.py             # Pytest fixtures, mock adapters, & report title hooks
│   ├── test_auth.py            # Authentication & header security tests
│   ├── test_weather.py         # Core GET /v1/weather happy path & functional tests
│   ├── test_current.py         # GET /v1/current conditions tests
│   ├── test_forecast.py        # GET /v1/forecast alias contract tests
│   ├── test_daily.py           # GET /v1/daily aggregated forecast tests
│   ├── test_hourly.py          # GET /v1/hourly forecast tests
│   ├── test_weather_geo.py     # Geo-targeting & IP lookup tests
│   ├── test_usage.py           # GET /v1/usage quota & billing tests
│   ├── test_error_handling.py  # Negative, edge-case, and boundary tests
│   ├── test_contracts.py       # JSON Schema validation tests
│   └── test_performance.py     # Latency & p95 performance threshold tests
│
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules protecting secrets & reports
├── LICENSE                     # MIT License
├── pytest.ini                  # Pytest configuration & markers
├── README.md                   # Complete framework documentation
└── requirements.txt            # Project dependencies
```

### Key Testing Categories Covered:
- **Authentication**: Valid token, missing header, invalid key, malformed Bearer header, empty Bearer token.
- **Functional Happy Path**: Parameterized coordinates (Nairobi, Tokyo, London, NY, Sydney), forecast day lengths (1..14), AI summaries, unit conversions (`metric` / `imperial`), localizations (`en` / `sw`).
- **Boundary & Edge Cases**: Latitude (-90.1, 90.1, non-numeric), Longitude (-180.1, 180.1, empty), Days (0, -1, 30, string), Units (`kelvin`), AI (`invalid_bool`).
- **Contract Testing**: `jsonschema` verification against OpenAPI / documentation schemas.
- **Performance**: Response time, average latency, and p95 calculations against configurable thresholds.
- **Rate-Limit Awareness**: Structural inspection of `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.

---

## 4. Test Coverage Summary

| Area | Endpoints / Modules Tested | Coverage Highlights |
| :--- | :--- | :--- |
| **Authentication** | `GET /v1/weather`, `GET /v1/usage` | Valid key, missing header, invalid key, malformed header, secret redaction |
| **Weather API** | `GET /v1/weather` | Global coordinates, day counts (1..14), unit systems, AI summaries, language |
| **Current Weather** | `GET /v1/current` | Real-time conditions, unit conversions |
| **Forecast Alias** | `GET /v1/forecast` | Contract equality validation against core `/v1/weather` endpoint |
| **Daily Forecast** | `GET /v1/daily` | Multi-day daily aggregated forecast structures |
| **Hourly Forecast** | `GET /v1/hourly` | Short-term hourly forecast resolution |
| **Geo & IP Lookup** | `GET /v1/weather-geo`, `GET /v1/ip-lookup` | Auto IP resolution (`?ip=auto`), explicit IPv4/IPv6, geo headers |
| **Usage API** | `GET /v1/usage` | Request counts (`used`, `limit`, `remaining`), AI counts, plan info, billing periods |
| **Error Handling** | All endpoints | 400 Bad Request client validation, 401 Unauthorized, 403 Forbidden, 429 Rate Limit |
| **Contract Validation**| `schemas/*.json` | Draft-07 JSON Schema validation for success and error responses |
| **Performance** | Core Weather Endpoints | Latency, batch average, p95 percentile vs `PERFORMANCE_THRESHOLD_MS` |
| **CI / CD Pipeline** | GitHub Actions | Automated runner, dependency caching, report artifact upload |

---

## 5. Prerequisites & Local Setup

### Prerequisites
- **Python**: Version 3.12 or higher installed.
- **API Key**: WeatherAI API key (`wai_...`).

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/weatherai-api-tests.git
   cd weatherai-api-tests
   ```

2. **Create and activate a virtual environment**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your credentials:
   ```env
   WEATHER_API_KEY=wai_your_actual_api_key_here
   WEATHER_API_BASE_URL=https://api.weather-ai.co
   API_TIMEOUT=10
   PERFORMANCE_THRESHOLD_MS=3000
   USE_MOCK_SERVER=false
   ```

---

## 6. Running Tests

### Run Full Test Suite
```bash
pytest
```

### Run in Verbose Mode
```bash
pytest -v
```

### Run Specific Test Category / File
```bash
pytest tests/test_weather.py
pytest tests/test_auth.py
pytest -m auth
pytest -m contract
```

### Generate Standalone HTML Test Report
```bash
pytest --html=reports/report.html --self-contained-html
```
The report will be generated at `reports/report.html`.

---

## 7. Exploratory QA Findings & Engineering Decisions

###  QA Finding 1: Production Host Returns 503 HTML Error
During initial exploratory probing of `https://api.weather-ai.co`, endpoints returned an HTTP 503 HTML page (`<html>...503 Server Error...The service you requested is not available yet...</html>`) rather than standard JSON-formatted error responses (`{"error": ...}`).
- **Impact**: Unhandled HTML errors break standard JSON parsers expecting `Content-Type: application/json`.
- **Framework Recommendation**: The API client inspects `Content-Type` before parsing JSON and raises a structured error. Additionally, a contract-compliant mock server adapter was introduced to ensure deterministic test execution during server downtime or CI runs.

###  Design Choice 1: Structural & Invariant Assertions Over Volatile Data
Weather measurements (temperature, wind speed, humidity) are highly volatile. Asserting exact values (e.g. `temperature == 24.5`) creates flaky tests. The framework validates **structural invariants**:
- Temperature must be numeric (`isinstance(temp, (int, float))`).
- Latitude must be in `[-90, 90]` and Longitude in `[-180, 180]`.
- Array length must equal the requested `days` count.
- Forecast dates must be valid ISO strings.

###  Design Choice 2: Secret Redaction & Sanitization Logger
To prevent API keys from leaking in test reports, console logs, or CI build logs:
- A custom `SecretSanitizingFormatter` in `utils/logger.py` automatically intercepts any pattern matching `wai_*` or `Bearer wai_*` and replaces it with `wai_***REDACTED***`.
- `.env` is strictly listed in `.gitignore`.

###  Design Choice 3: Protection of Monthly Quota
To prevent test runs from depleting customer quota:
- Rate-limit testing inspects response headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) rather than firing 50,000 requests to trigger a 429 status code.

---

## 8. Known Limitations

1. **Scale / Pro Plan Restrictions**: SMS endpoints (`/v1/sms/send`) and multi-crop tree crown analysis (`/v1/trees/analyze`) require active Scale or Pro subscriptions. Tests for these endpoints are marked as skipped contract assertions when run on Free plan keys.
2. **Live Server Availability**: As noted in QA Finding 1, live execution against `https://api.weather-ai.co` depends on backend service deployment state.

---

## 9. Future Improvements

- **Dedicated Staging Environment Integration**: Configure environment-based target switching (`STAGING` vs `PRODUCTION`).
- **Parallel Execution**: Integrate `pytest-xdist` for multi-threaded test execution.
- **Contract Schema Registry**: Synchronize JSON Schemas directly with an OpenAPI / Swagger spec repository.
- **Mutation Testing**: Introduce `mutmut` to evaluate test suite assertion strength.
