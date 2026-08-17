# Рівень Б: Наскрізна Sequence-діаграма локалізації (i18n Full-Stack Sequence)

> **Призначення**: Повний цикл перемикання мови між словниками `i18n.js`, оновленням усього DOM-дерева, перекладом модалок і динамічних бейджів.

---

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Користувач
    participant LangBtns as 🌐 #langBtnUk / #langBtnEn
    participant I18n as 📖 I18n Module (i18n.js)
    participant DOM as 🖥️ DOM Elements
    participant TreeRend as 🌳 TreeRenderer
    participant SideCtrl as 📑 SidebarController
    participant ModalMgr as 🪟 ModalManager

    %% 1. Перемикання на Англійську мову
    Note over User, ModalMgr: ФАЗА 1: Перемикання інтерфейсу на англійську мову (EN)
    User ->> LangBtns: Клік на кнопку "EN" (#langBtnEn)
    LangBtns ->> I18n: setLanguage('en')
    I18n ->> I18n: this.currentLang = 'en', localStorage.setItem('je_lang', 'en')
    I18n ->> LangBtns: Додавання .active до #langBtnEn, зняття з #langBtnUk
    I18n ->> DOM: I18n.updateDOM()
    DOM ->> DOM: Оновлення всіх data-i18n ("Tree", "Settings", "Import Excel"...)
    I18n ->> TreeRend: re-renderTree() -> оновлення бейджів типів ("Currency", "Date"...)
    I18n ->> SideCtrl: filterAndRenderSidebar() -> оновлення бейджів колонок
    I18n ->> ModalMgr: Оновлення текстів заголовків і кнопок модальних вікон
    DOM -->> User: Весь інтерфейс миттєво перекладено на англійську мову

    %% 2. Перемикання назад на Українську мову
    Note over User, ModalMgr: ФАЗА 2: Повернення інтерфейсу на українську мову (UK)
    User ->> LangBtns: Клік на кнопку "UA" (#langBtnUk)
    LangBtns ->> I18n: setLanguage('uk')
    I18n ->> I18n: this.currentLang = 'uk', localStorage.setItem('je_lang', 'uk')
    I18n ->> LangBtns: Додавання .active до #langBtnUk, зняття з #langBtnEn
    I18n ->> DOM: I18n.updateDOM()
    DOM ->> DOM: Тексти стають ("Дерево", "Налаштування", "Імпорт Excel"...)
    I18n ->> TreeRend: re-renderTree() -> бейджі ("Валюта", "Дата"...)
    I18n ->> SideCtrl: filterAndRenderSidebar()
    DOM -->> User: Інтерфейс повернуто до української мови
```
