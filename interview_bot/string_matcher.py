def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_closest_match(input_str, valid_strings, threshold=0.7):
    """Find the closest matching string from a list of valid strings
    Returns (best_match, similarity_score)"""
    input_str = input_str.lower()
    
    # First try exact match after normalization
    for valid in valid_strings:
        if valid.lower() == input_str:
            return valid, 1.0
            
    # Direct substring match
    matches = [v for v in valid_strings if input_str in v.lower() or v.lower() in input_str]
    if matches:
        return matches[0], 0.9
        
    # Try fuzzy matching
    best_match = None
    best_score = 0
    
    for valid in valid_strings:
        # Calculate normalized similarity score
        max_len = max(len(input_str), len(valid.lower()))
        if max_len == 0:
            continue
        distance = levenshtein_distance(input_str, valid.lower())
        similarity = 1 - (distance / max_len)
        
        if similarity > best_score:
            best_score = similarity
            best_match = valid
    
    if best_score >= threshold:
        return best_match, best_score
    return None, best_score