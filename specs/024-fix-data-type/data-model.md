# Data Model & Interface: Data Type Badge Localization

**Feature Branch**: `024-fix-data-type`  
**Spec**: [specs/024-fix-data-type/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. `I18n` Engine Extended Method

```typescript
interface I18nExtended extends I18nEngine {
    getTypeLabel(type: string | null | undefined): string;
}
```

---

## 2. DOM Rendering Contract

```html
<!-- Tree Canvas Node Badge -->
<span class="node-type-badge" data-type="Text" title="Тип даних колонки Excel (Подвійний клік для зміни)">
    Текст (Рядок)
</span>

<!-- Sidebar Catalog Header Tag -->
<span class="header-type-tag" title="Тип даних колонки Excel (Подвійний клік для зміни)">
    Текст (Рядок)
</span>

<!-- Paths Export Preview Tag -->
<span class="node-type-badge" data-type="Text" title="Тип даних колонки Excel (Подвійний клік для зміни)">
    Текст (Рядок)
</span>
```
