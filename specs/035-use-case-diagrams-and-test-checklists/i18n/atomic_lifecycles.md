# Рівень А: Атомарні мікро-цикли елементів (i18n Micro-Lifecycles)

> **Призначення**: Автомати станів для перемикача мов, оновлення DOM-атрибутів та локалізованих бейджів.

---

## 1. `LanguageToggleLifecycle` (Життєвий цикл кнопок вибору мови)

Застосовується до: `#langBtnUk`, `#langBtnEn`.

```mermaid
stateDiagram-v2
    [*] --> UkActive: Initial ("uk") -> #langBtnUk.active
    UkActive --> SwitchingToEn: Click #langBtnEn
    SwitchingToEn --> EnActive: I18n.setLanguage('en') -> #langBtnEn.active, #langBtnUk inactive
    EnActive --> SwitchingToUk: Click #langBtnUk
    SwitchingToUk --> UkActive: I18n.setLanguage('uk') -> #langBtnUk.active, #langBtnEn inactive
```

---

## 2. `DOMTranslationTraversalLifecycle` (Життєвий цикл перекладу DOM)

Застосовується до: `document.querySelectorAll('[data-i18n], [data-i18n-title], [data-i18n-placeholder]')`.

```mermaid
stateDiagram-v2
    [*] --> EventFired: 'languageChanged' event dispatched
    EventFired --> QueryingElements: Select all tagged elements in DOM
    QueryingElements --> UpdatingText: element.textContent = I18n.t(key)
    UpdatingText --> UpdatingTitles: element.title = I18n.t(titleKey)
    UpdatingTitles --> UpdatingPlaceholders: input.placeholder = I18n.t(placeholderKey)
    UpdatingPlaceholders --> UpdateComplete: Visual state fully localized
```

---

## 3. `DynamicBadgeTranslatorLifecycle` (Життєвий цикл локалізації динамічних бейджів)

Застосовується до: `.type-badge` на вузлах та в сайдбарі.

```mermaid
stateDiagram-v2
    [*] --> TypeKeyStored: Node data-type = "Currency"
    TypeKeyStored --> RenderingInUk: I18n.getTypeLabel("Currency") -> "Валюта"
    RenderingInUk --> LanguageSwapped: Switch to EN
    LanguageSwapped --> RenderingInEn: I18n.getTypeLabel("Currency") -> "Currency"
    RenderingInEn --> LanguageSwappedBack: Switch to UK
    LanguageSwappedBack --> RenderingInUk: "Валюта"
```
