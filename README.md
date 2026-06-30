# Goszakup Auto-Application Bot

⚠️ **Дисклеймер**: Этот репозиторий является витриной кода для демонстрации. URL endpoint'ов, XPath/CSS-селекторы и структуры payload'ов форм намеренно скрыты или упрощены. Полная реализация доступна только заказчику.

Система автоматической подачи заявок на портал госзакупок Республики Казахстан (goszakup.gov.kz).

## Архитектура

### State Machine Pattern

Каждый HTTP-запрос сопровождается проверкой состояния через `PageDetector`:

```
INIT -> COOKIES_LOADED -> ANNOUNCE_VALID -> CONTEXT_READY -> ANNEXES_PROCESSING -> COMPLETE
```

### ErrorClassifier

Система классификации ошибок:
- `SESSION_RESET` — сессия истекла, требуется повторная авторизация
- `ANNOUNCE_NOT_FOUND` — объявление не найдено или недоступно
- `ANNOUNCE_CLOSED` — прием заявок завершен
- `VALIDATION_ERROR` — ошибка валидации формы
- `NETWORK_ERROR` — проблемы с сетью

### Core Components

#### AsyncSessionManager
- Асинхронное управление HTTP-сессией (aiohttp)
- Автоматическое обновление cookies
- SSL-контекст для работы с порталом

#### PageDetector
- Определение текущего состояния страницы
- Проверка наличия капчи, ошибок авторизации
- Валидация структуры ответа

#### AnnexProcessor
- Обработка приложений 1, 2, 4, 11, 15, 19
- Параллельная обработка (asyncio.gather)
- Автоматическая подпись документов

#### KalkanSigner
- Интеграция с KalkanCrypt SDK
- Подпись CMS через XML-RPC
- Headless-режим для автоматизации

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

- Сигналы/слоты для асинхронного обновления UI
- Потокобезопасное логирование через QtHandler
- Таймеры для мониторинга статуса

## Структура проекта

```
gitversion/
├── main.py                 # Точка входа
├── gui.py                  # PyQt6 интерфейс
├── requirements.txt        # Зависимости
├── src/
│   ├── core/
│   │   ├── async_annexes.py      # Обработка приложений
│   │   ├── async_session.py      # HTTP-сессия
│   │   ├── error_classifier.py   # Классификация ошибок
│   │   ├── page_detector.py      # Детектор состояний
│   │   └── kalkan_headless.py    # Подпись документов
│   └── utils/
│       └── path_resolver.py      # Управление путями
└── core/
    ├── har_config.json           # HAR-конфигурация
    └── har_patterns.json         # Паттерны запросов
```

## Технологический стек

- **Python 3.8+** — основной язык
- **asyncio / aiohttp** — асинхронные HTTP-запросы
- **PyQt6** — графический интерфейс
- **BeautifulSoup4 / lxml** — парсинг HTML
- **KalkanCrypt** — электронная подпись (ЭЦП)

## Code Style

- **PEP 8** — стандарт оформления
- **Type Hints** — аннотации типов для всех функций
- **Docstrings** — Google-style документация
- **Async/await** — строго асинхронная архитектура

## Безопасность

Конкретные URL endpoint'ов, XPath/CSS-селекторы и структуры payload'ов форм намеренно скрыты. Полная реализация доступна только заказчику.
