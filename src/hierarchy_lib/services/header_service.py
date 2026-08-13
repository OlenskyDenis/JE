"""HeaderService for processing, deduplicating, sorting, and filtering Excel Row 1 headers."""

from typing import List, Any, Optional


class HeaderService:
    """Service responsible for Header list operations."""

    @staticmethod
    def process_headers(raw_headers: List[Any]) -> List[str]:
        """Cleans, trims whitespace, removes empty values, deduplicates, and sorts headers alphabetically."""
        seen = set()
        cleaned_headers: List[str] = []

        for item in raw_headers:
            if item is None:
                continue
            item_str = str(item).strip()
            if not item_str:
                continue
            if item_str not in seen:
                seen.add(item_str)
                cleaned_headers.append(item_str)

        # Sort case-insensitively while preserving original string casing
        cleaned_headers.sort(key=lambda s: (s.lower(), s))
        return cleaned_headers

    @staticmethod
    def filter_headers(headers: List[str], query: Optional[str]) -> List[str]:
        """Filters header list by case-insensitive substring search query."""
        if not query or not query.strip():
            return headers
        q = query.strip().lower()
        return [h for h in headers if q in h.lower()]
