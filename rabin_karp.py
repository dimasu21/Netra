"""
Rabin-Karp Algorithm Implementation
===================================
A custom implementation of the Rabin-Karp string searching algorithm
using Rolling Hash technique.

This module is designed for the "Smart Physical Doc Search" project
to demonstrate understanding of the algorithm for thesis purposes.

DO NOT use Python's built-in find() or index() methods.
"""


# =============================================================================
# ROLLING HASH CONSTANTS
# =============================================================================

# Base value for polynomial hash (number of characters in alphabet)
# Using 256 for extended ASCII character set
BASE = 256

# Prime number for modulo operation to reduce hash collisions
# A prime number helps distribute hash values more uniformly
PRIME = 101


# =============================================================================
# RABIN-KARP ALGORITHM
# =============================================================================

def rabin_karp_search(text: str, pattern: str) -> list:
    """
    Search for all occurrences of a pattern in text using Rabin-Karp algorithm.
    
    The Rabin-Karp algorithm uses a rolling hash to efficiently compare
    substrings. Instead of comparing characters one by one, it computes
    a hash value for the pattern and compares it with hash values of
    substrings of the same length in the text.
    
    ROLLING HASH FORMULA:
    ====================
    For a string s[0..m-1], the hash is computed as:
    
        hash(s) = (s[0] * BASE^(m-1) + s[1] * BASE^(m-2) + ... + s[m-1] * BASE^0) mod PRIME
    
    When sliding the window by one character:
    
        new_hash = ((old_hash - s[i] * BASE^(m-1)) * BASE + s[i+m]) mod PRIME
    
    This allows O(1) hash update instead of O(m) recalculation.
    
    Args:
        text (str): The text to search within
        pattern (str): The pattern to search for
        
    Returns:
        list: List of starting indices where pattern is found
    """
    # Handle edge cases
    if not pattern or not text:
        return []
    
    if len(pattern) > len(text):
        return []
    
    # Convert to lowercase for case-insensitive search
    text = text.lower()
    pattern = pattern.lower()
    
    n = len(text)      # Length of text
    m = len(pattern)   # Length of pattern
    
    # List to store found positions
    found_positions = []
    
    # Calculate hash value for pattern
    pattern_hash = 0
    
    # Calculate hash value for first window of text
    text_hash = 0
    
    # Precompute BASE^(m-1) mod PRIME
    # This value is used to remove the leading digit when sliding the window
    h = 1
    for _ in range(m - 1):
        h = (h * BASE) % PRIME
    
    # Calculate initial hash values for pattern and first window of text
    # hash = (char[0] * BASE^(m-1) + char[1] * BASE^(m-2) + ... + char[m-1]) mod PRIME
    for i in range(m):
        pattern_hash = (BASE * pattern_hash + ord(pattern[i])) % PRIME
        text_hash = (BASE * text_hash + ord(text[i])) % PRIME
    
    # Slide the pattern over text one character at a time
    for i in range(n - m + 1):
        # If hash values match, verify with actual string comparison
        # (to handle hash collisions - "spurious hits")
        if pattern_hash == text_hash:
            # Character-by-character comparison to confirm match
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            
            if match:
                found_positions.append(i)
        
        # Calculate hash for next window using rolling hash
        # Only if we're not at the last position
        if i < n - m:
            # Rolling hash formula:
            # 1. Remove leading character: (old_hash - leading_char * h)
            # 2. Shift left: multiply by BASE
            # 3. Add trailing character: add new_char
            # 4. Apply modulo
            
            leading_char = ord(text[i])
            trailing_char = ord(text[i + m])
            
            text_hash = (BASE * (text_hash - leading_char * h) + trailing_char) % PRIME
            
            # Handle negative hash values (Python handles negative mod, but being explicit)
            if text_hash < 0:
                text_hash += PRIME
    
    return found_positions


def highlight_matches(text: str, pattern: str) -> str:
    """
    Find all occurrences of pattern in text and wrap them with <mark> tags.
    
    This function preserves the original case of the text while performing
    case-insensitive search.
    
    Args:
        text (str): The original text
        pattern (str): The pattern to search for and highlight
        
    Returns:
        str: Text with matched patterns wrapped in <mark> tags
    """
    if not pattern or not text:
        return text
    
    # Find all positions using Rabin-Karp
    positions = rabin_karp_search(text, pattern)
    
    if not positions:
        return text
    
    # Build highlighted text
    # We need to work from end to start to preserve indices
    result = text
    pattern_len = len(pattern)
    
    # Sort positions in reverse order to maintain correct indices while inserting
    for pos in sorted(positions, reverse=True):
        # Extract the original text (preserving case)
        original_match = result[pos:pos + pattern_len]
        # Wrap with <mark> tags
        highlighted = f"<mark>{original_match}</mark>"
        # Replace in result
        result = result[:pos] + highlighted + result[pos + pattern_len:]
    
    return result


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_match_count(text: str, pattern: str) -> int:
    """
    Count the number of times pattern appears in text.
    
    Args:
        text (str): The text to search within
        pattern (str): The pattern to count
        
    Returns:
        int: Number of occurrences
    """
    return len(rabin_karp_search(text, pattern))


def get_match_info(text: str, pattern: str) -> dict:
    """
    Get detailed information about pattern matches in text.
    
    Args:
        text (str): The text to search within
        pattern (str): The pattern to search for
        
    Returns:
        dict: Dictionary containing match information
    """
    positions = rabin_karp_search(text, pattern)
    
    return {
        'pattern': pattern,
        'count': len(positions),
        'positions': positions,
        'found': len(positions) > 0
    }


# =============================================================================
# TEST / DEMO
# =============================================================================

if __name__ == "__main__":
    # Demo the algorithm
    test_text = "The quick brown fox jumps over the lazy dog. The dog sleeps."
    test_pattern = "the"
    
    print(f"Text: {test_text}")
    print(f"Pattern: '{test_pattern}'")
    print(f"Positions found: {rabin_karp_search(test_text, test_pattern)}")
    print(f"Highlighted: {highlight_matches(test_text, test_pattern)}")
