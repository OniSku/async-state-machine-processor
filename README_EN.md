# Goszakup Auto-Application Bot

⚠️ **Disclaimer**: This repository serves as a code showcase for demonstration purposes. Endpoint URLs, XPath/CSS selectors, and form payload structures are intentionally omitted or simplified. The full implementation is available to the client only.

Automated application submission system for the Public Procurement Portal of the Republic of Kazakhstan (goszakup.gov.kz).

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ |
| HTTP | asyncio / aiohttp |
| GUI | PyQt6 |
| HTML parsing | BeautifulSoup4 / lxml |
| Digital signature | KalkanCrypt SDK (XML-RPC) |

## Architecture

### State Machine

Each HTTP request is validated against the current portal state via `PageDetector`:

```
INIT -> COOKIES_LOADED -> ANNOUNCE_VALID -> CONTEXT_READY -> ANNEXES_PROCESSING -> COMPLETE
```

### ErrorClassifier

Classifies runtime errors into recoverable categories:

- `SESSION_RESET` — session expired, re-authentication required
- `ANNOUNCE_NOT_FOUND` — announcement not found or inaccessible
- `ANNOUNCE_CLOSED` — application submission period closed
- `VALIDATION_ERROR` — form validation failure
- `NETWORK_ERROR` — network-level failure

### Core Components

**AsyncSessionManager**
- Async HTTP session management via aiohttp
- Automatic cookie refresh
- SSL context configured for the portal's certificate chain

**PageDetector**
- Detects current portal page state
- Checks for CAPTCHA presence and authorization errors
- Validates response structure

**AnnexProcessor**
- Processes annexes 1, 2, 4, 11, 15, 19
- Parallel processing via `asyncio.gather`
- Automatic document signing

**KalkanSigner**
- Integration with KalkanCrypt SDK
- CMS signing via XML-RPC
- Headless mode for unattended automation

### GUI Architecture (PyQt6)

```
MainWindow
├── Worker (QThread)
│   ├── AsyncSessionManager
│   ├── AnnexProcessor
│   └── KalkanSigner
├── QueueManager
└── ConfigManager
```

- Signals/slots for async UI updates
- Thread-safe logging via `QtHandler`
- Status monitoring via timers

## Project Structure

```
gitversion/
├── gui.py                        # PyQt6 interface and main window
├── requirements.txt
├── src/
│   ├── core/
│   │   ├── async_annexes.py      # Annex processing
│   │   ├── async_session.py      # HTTP session management
│   │   ├── error_classifier.py   # Error classification
│   │   ├── page_detector.py      # State detection
│   │   └── kalkan_headless.py    # Document signing
│   └── utils/
│       └── path_resolver.py      # Path management
└── core/
    ├── har_config.json           # HAR configuration (sanitized)
    └── har_patterns.json         # Request patterns (sanitized)
```

## Installation & Setup

```bash
pip install -r requirements.txt
```

Copy and fill in the configuration:

```bash
cp config.example.ini config.ini
```

| Parameter | Description |
|---|---|
| `login` | Portal account login |
| `password` | Portal account password |
| `announce_number` | Procurement announcement number |
| `kalkan_path` | Path to KalkanCrypt installation |
| `certificate_path` | Path to EDS certificate file |
| `certificate_password` | EDS certificate password |

Run the GUI:

```bash
python gui.py
```

## Code Style

- PEP 8
- Type hints on all functions
- Google-style docstrings
- Strictly async architecture (async/await throughout)
