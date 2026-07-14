import os
from wordfreq import zipf_frequency

# -------------------------------------------------------------------
# 1. Load Local SOWPODS Dictionary File
# -------------------------------------------------------------------

SOWPODS_FILE = "FILE PATH"

def load_sowpods_dictionary() -> list[str]:
    """Reads the local sowpods.txt file into a list of strings."""
    if not os.path.exists(SOWPODS_FILE):
        raise FileNotFoundError(
            f"Could not find '{SOWPODS_FILE}'. Make sure you saved sowpods.txt "
            f"in the exact same directory as this Python script!"
        )
        
    with open(SOWPODS_FILE, "r", encoding="utf-8") as f:
        # Lowercase words and remove empty lines / whitespace
        words = [line.strip().lower() for line in f if line.strip()]
    return words

# Initialize dictionary from the local file
DICTIONARY = load_sowpods_dictionary()


# -------------------------------------------------------------------
# 2. Condition / Filter Functions
# -------------------------------------------------------------------

def condition_contains(substring: str) -> set[str]:
    """Returns words containing the given substring."""
    sub = substring.lower()
    return {w for w in DICTIONARY if sub in w}

def condition_does_not_contain(forbidden_letters):
    """
    Excludes words containing ANY of the specified letters.
    Example: forbidden_letters="abc" or ["a", "b", "c"]
    """
    letters = set(forbidden_letters.lower())
    return {w for w in DICTIONARY if not any(c in w for c in letters)}

def condition_ends_with(suffix: str) -> set[str]:
    """Returns words ending with the given suffix."""
    suf = suffix.lower()
    return {w for w in DICTIONARY if w.endswith(suf)}

def condition_starts_with(prefix: str) -> set[str]:
    """Returns words starting with the given prefix."""
    pre = prefix.lower()
    return {w for w in DICTIONARY if w.startswith(pre)}

def condition_min_occurrences(char: str, count: int) -> set[str]:
    """Returns words containing a character at least `count` times."""
    c = char.lower()
    return {w for w in DICTIONARY if w.count(c) >= count}

def condition_length(length: int) -> set[str]:
    """Returns words of an exact length."""
    return {w for w in DICTIONARY if len(w) == length}

def condition_length_range(min_len, max_len):
    """Returns words whose length is between min_len and max_len (inclusive)."""
    return {w for w in DICTIONARY if min_len <= len(w) <= max_len}

def condition_multiple_letter_count(letter):
    return {w for w in DICTIONARY if w.count(letter) >= 2}

def condition_letter_at_index(char, index):
    """Word has a specific character at a zero-indexed position (e.g. 'a' at index 1 -> 'xAx...')"""
    c = char.lower()
    return {w for w in DICTIONARY if len(w) > index and w[index] == c}

def condition_exact_occurrences(char, count):
    """Word contains a character EXACTLY `count` times (not 'at least')."""
    c = char.lower()
    return {w for w in DICTIONARY if w.count(c) == count}

def condition_starts_and_ends(prefix, suffix):
    """Word starts with one substring and ends with another."""
    pre, suf = prefix.lower(), suffix.lower()
    return {w for w in DICTIONARY if w.startswith(pre) and w.endswith(suf)}


# -------------------------------------------------------------------
# 3. Intersection & Ranking Logic
# -------------------------------------------------------------------

def get_rarest_words(set_a: set[str], set_b: set[str]) -> list[tuple[str, float]]:
    """
    Finds the set intersection of two conditions and ranks them by Zipf score (lowest first).
    """
    valid_words = set_a.intersection(set_b)
    
    if not valid_words:
        return []
    
    # Sort by Zipf frequency (0.0 = ultra-rare/obscure, higher = common)
    ranked_words = sorted(
        valid_words,
        key=lambda w: zipf_frequency(w, "en")
    )
    
    return [(word, zipf_frequency(word, "en")) for word in ranked_words[:20]]


# -------------------------------------------------------------------
# 4. Example Usage
# -------------------------------------------------------------------

if __name__ == "__main__":
    row_words = condition_ends_with("er")
    col_words = condition_multiple_letter_count("l")
    
    rarest_matches = get_rarest_words(row_words, col_words)
    
    print("\n--- Rarest Words at Grid Intersection ---")
    for word, score in rarest_matches:
        print(f" • {word:<15} (Zipf score: {score:.2f})")
