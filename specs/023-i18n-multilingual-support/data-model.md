# Data Model & Contracts: I18n Localization Engine

**Feature Branch**: `023-i18n-multilingual-support`  
**Spec**: [specs/023-i18n-multilingual-support/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. `I18n` JavaScript Interface Contract

```typescript
interface I18nEngine {
    currentLanguage: 'uk' | 'en';
    
    // Core Translation Lookup
    t(key: string, params?: Record<string, string | number>): string;
    
    // Switch Active Locale & Trigger DOM Refresh
    setLanguage(lang: 'uk' | 'en'): void;
    
    // Get Current Locale
    getLanguage(): 'uk' | 'en';
    
    // Declarative DOM Tree Translator
    translateDOM(rootElement?: HTMLElement): void;
    
    // Register UI Update Callback (Observer Pattern)
    onLanguageChanged(callback: (lang: 'uk' | 'en') => void): void;
}
```

---

## 2. Declarative HTML Data Attributes

| Attribute | Example | Behavior |
|---|---|---|
| `data-i18n` | `<span data-i18n="brand_title"></span>` | Sets `element.textContent = I18n.t(key)` |
| `data-i18n-attr` | `<input data-i18n-attr="placeholder:catalog_search_placeholder;title:search_title">` | Parses semicolon-delimited `attr:key` pairs and updates DOM attributes |

---

## 3. Storage Schema

- Key in `localStorage`: `"app_language"`
- Allowed values: `"uk"` | `"en"`
- Default on first boot: `"uk"`
