"""Module for matching patterns and extracting structured data from text."""
import re
from typing import List, Dict, Any


class PatternMatcher:
    """Extracts structured data from text based on keyword patterns."""
    
    def __init__(self, keywords: List[str]):
        """
        Initialize pattern matcher with keywords.
        
        Args:
            keywords: List of keywords to search for (e.g., ["ID", "Color", "Model", "Year"])
        """
        self.keywords = keywords
        if not keywords:
            raise ValueError("Keywords list cannot be empty")
    
    def extract_records(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract structured records from text based on keywords.
        
        The pattern expected is: "Keyword1: value1 Keyword2: value2 ..."
        Records are separated when a new occurrence of the first keyword is found.
        
        Args:
            text: Text content to extract from
            
        Returns:
            List of dictionaries, each containing the extracted key-value pairs
        """
        if not self.keywords:
            return []
        
        first_keyword = self.keywords[0]
        records = []
        current_record = {}
        
        # Create a regex pattern to match all keywords
        # Pattern: "Keyword: value" (case-insensitive, flexible whitespace)
        keyword_patterns = {}
        for keyword in self.keywords:
            # Escape special regex characters in keyword
            escaped_keyword = re.escape(keyword)
            # Match "Keyword:" followed by optional whitespace and then the value
            # Value continues until next keyword or end of line/string
            pattern = rf"{escaped_keyword}\s*:\s*([^\n]+?)(?=\s*(?:{'|'.join([re.escape(k) for k in self.keywords])})\s*:|$)"
            keyword_patterns[keyword] = re.compile(pattern, re.IGNORECASE)
        
        # Split text into potential record sections
        # Look for occurrences of the first keyword to identify record boundaries
        first_keyword_pattern = re.compile(
            rf"\b{re.escape(first_keyword)}\s*:",
            re.IGNORECASE
        )
        
        # Find all positions where a new record might start
        matches = list(first_keyword_pattern.finditer(text))
        
        if not matches:
            # Try to extract a single record if no clear boundaries found
            record = self._extract_single_record(text, keyword_patterns)
            if record:
                records.append(record)
            return records
        
        # Process each potential record
        for i, match in enumerate(matches):
            # Get text from this match to the next match (or end of text)
            start_pos = match.start()
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(text)
            
            record_text = text[start_pos:end_pos]
            record = self._extract_single_record(record_text, keyword_patterns)
            
            if record:
                records.append(record)
        
        return records
    
    def _extract_single_record(self, text: str, keyword_patterns: Dict[str, re.Pattern]) -> Dict[str, Any]:
        """
        Extract a single record from a text snippet.
        
        Args:
            text: Text snippet containing one record
            keyword_patterns: Dictionary of compiled regex patterns for each keyword
            
        Returns:
            Dictionary with extracted key-value pairs
        """
        record = {}
        
        for keyword, pattern in keyword_patterns.items():
            match = pattern.search(text)
            if match:
                value = match.group(1).strip()
                # Clean up value (remove trailing colons, extra whitespace)
                value = re.sub(r'\s+', ' ', value).strip()
                if value:
                    record[keyword] = value
        
        # Only return record if it has at least the first keyword
        if self.keywords and self.keywords[0] in record:
            return record
        
        return None

