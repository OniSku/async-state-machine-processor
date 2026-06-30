# Goszakup Auto-Application Bot

⚠️ **Дисклеймер**: Этот репозиторий является витриной кода для демонстрации. URL endpoint'ов, XPath/CSS-селекторы и структуры payload'ов форм намеренно скрыты или упрощены. Полная реализация доступна только заказчику.

> **NDA**: Исходный код в этом репозитории является витринной версией. Полная реализация, бизнес-логика и конфигурации, специфичные для заказчика, являются проприетарными и охраняются соглашением о неразглашении.

Система автоматической подачи заявок на портал госзакупок Республики Казахстан (goszakup.gov.kz).

## Стек технологий

| Компонент | Технология |
|---|---|
| Язык | Python 3.8+ |
| HTTP | asyncio / aiohttp |
| GUI | PyQt6 |
| Парсинг HTML | BeautifulSoup4 / lxml |
| Электронная подпись | KalkanCrypt SDK (XML-RPC) |

## Архитектура

### State Machine

Каждый HTTP-запрос проверяется через `PageDetector` на соответствие текущему состоянию портала:

```
INIT -> COOKIES_LOADED -> ANNOUNCE_VALID -> CONTEXT_READY -> ANNEXES_PROCESSING -> COMPLETE
```

### ErrorClassifier

Классифицирует ошибки выполнения по восстанавливаемым категориям:

- `SESSION_RESET` — сессия истекла, требуется повторная авторизация
- `ANNOUNCE_NOT_FOUND` — объявление не найдено или недоступно
- `ANNOUNCE_CLOSED` — приём заявок завершён
- `VALIDATION_ERROR` — ошибка валидации формы
- `NETWORK_ERROR` — сетевая ошибка

### Основные компоненты

**AsyncSessionManager**
- Асинхронное управление HTTP-сессией через aiohttp
- Автоматическое обновление cookies
- SSL-контекст, настроенный под цепочку сертификатов портала

**PageDetector**
- Определение текущего состояния страницы портала
- Проверка наличия CAPTCHA и ошибок авторизации
- Валидация структуры ответа

**AnnexProcessor**
- Обработка приложений 1, 2, 4, 11, 15, 19
- Параллельная обработка через `asyncio.gather`
- Автоматическая подпись документов

**KalkanSigner**
- Интеграция с KalkanCrypt SDK
- Подпись CMS через XML-RPC
- Headless-режим для автоматизированной работы

### GUI-архитектура (PyQt6)

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
- Потокобезопасное логирование через `QtHandler`
- Мониторинг статуса через таймеры

## Структура проекта

```
gitversion/
├── gui.py                        # PyQt6-интерфейс и главное окно
├── requirements.txt
├── src/
│   ├── core/
│   │   ├── async_annexes.py      # Обработка приложений
│   │   ├── async_session.py      # Управление HTTP-сессией
│   │   ├── error_classifier.py   # Классификация ошибок
│   │   ├── page_detector.py      # Детектор состояний
│   │   └── kalkan_headless.py    # Подпись документов
│   └── utils/
│       └── path_resolver.py      # Управление путями
└── core/
    ├── har_config.json           # HAR-конфигурация (санированная)
    └── har_patterns.json         # Паттерны запросов (санированные)
```

## Установка и запуск

```bash
pip install -r requirements.txt
```

Скопируйте конфигурацию:

```bash
cp config.example.ini config.ini
```

| Параметр | Описание |
|---|---|
| `login` | Логин аккаунта на портале |
| `password` | Пароль аккаунта |
| `announce_number` | Номер закупочного объявления |
| `kalkan_path` | Путь к установке KalkanCrypt |
| `certificate_path` | Путь к файлу ЭЦП-сертификата |
| `certificate_password` | Пароль ЭЦП-сертификата |

Запуск GUI:

```bash
python gui.py
```

## Стиль кода

- PEP 8
- Type hints на всех функциях
- Docstrings в Google-style
- Строго асинхронная архитектура (async/await везде)
