# Define the four sides of the Letterboxed square (Example: Change these per puzzle)
side_1 = "nom"
side_2 = "ize"
side_3 = "stb"
side_4 = "yla"

# Load wordlist from file
wordlist_path = r'PATH:\wordlist.txt'  # Change path

from collections import defaultdict, deque

# Load word list
def load_words(filepath):
    """Load words from a text file, assuming one word per line."""
    with open(filepath, "r") as f:
        words = set(word.strip().lower() for word in f)
    return words

# Function to filter words based on Letterboxed letters
def filter_words(wordlist, allowed_letters):
    """Return words that only contain letters from allowed_letters."""
    allowed_set = set(allowed_letters)
    return {word for word in wordlist if set(word).issubset(allowed_set)}

def filter_valid_words(wordlist):
    
    return {word for word in wordlist if len(word) > 2}

def is_valid_word(word, sides):
    """
    - No two consecutive letters can come from the same side.
    
    Parameters:
    word (str): The word to check.
    sides (list): List of 4 sets, each representing one side of the square.
    
    Returns:
    bool: True if the word follows the rule, False otherwise.
    """
    for i in range(len(word) - 1):
        # Find which side each letter belongs to
        letter1_side = next(index for index, side in enumerate(sides) if word[i] in side)
        letter2_side = next(index for index, side in enumerate(sides) if word[i + 1] in side)
        
        # If two consecutive letters are from the same side, it's invalid
        if letter1_side == letter2_side:
            return False
    
    return True

def build_word_graph(words):
    """
    Build a directed graph where words are nodes and edges exist if
    the last letter of one word matches the first letter of another.
    
    Parameters:
    words (set): The set of valid words.
    
    Returns:
    dict: Adjacency list representing the graph.
    """
    graph = defaultdict(list)
    
    for word1 in words:
        last_letter = word1[-1]  # Last letter of current word
        for word2 in words:
            if word1 != word2 and word2[0] == last_letter:
                graph[word1].append(word2)
    
    return graph

def find_multiple_letterboxed_solutions(word_graph, letterboxed_letters, max_length=6, solution_limit=3):
    """
    Finds multiple valid solutions that cover all Letterboxed letters.
    """
    target_letters = set(letterboxed_letters)
    queue = deque([(word, [word], set(word)) for word in word_graph])
    solutions = []

    while queue and len(solutions) < solution_limit:
        current_word, path, used_letters = queue.popleft()

        # Check if this path covers all required letters
        if used_letters >= target_letters:
            solutions.append(path)
            continue  # Keep searching for more solutions

        # Stop expanding if we reach max_length
        if len(path) >= max_length:
            continue

        # Add next words to the queue, avoiding duplicates
        for next_word in word_graph[current_word]:
            if next_word not in path:  # Avoid cycles
                new_used_letters = used_letters | set(next_word)
                queue.append((next_word, path + [next_word], new_used_letters))

    return solutions

#store list of words
all_words = load_words(wordlist_path)

# Combine all letters into a single set for filtering
letterboxed_letters = side_1 + side_2 + side_3 + side_4
valid_words = filter_words(all_words, letterboxed_letters)

# Get the filtered words
valid_words_strict = filter_valid_words(valid_words)

# Verify that no 1- or 2-letter words are included
#print("Filtered words (first 20):", list(valid_words_strict)[:20])

# Convert sides to sets for faster lookup
sides = [set(side_1), set(side_2), set(side_3), set(side_4)]

# Filter words that follow Letterboxed rules
valid_words_strict = {word for word in valid_words_strict if is_valid_word(word, sides)}

#print(f"After enforcing Letterboxed rules, {len(valid_words_strict)} words remain.")
#print("Sample valid words:", list(valid_words_strict)[:10])

# Build graph from the strictly valid words
word_graph = build_word_graph(valid_words_strict)

# Print some connections to verify
#print("Sample word transitions:")
#for word, next_words in list(word_graph.items())[:10]:
#    print(f"{word} → {next_words}")

# Run the search
solutions = find_multiple_letterboxed_solutions(word_graph, letterboxed_letters, solution_limit=10)

print("Searching for solutions....")

# Print results
if solutions:
    print(f"Found {len(solutions)} solutions:")
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i} ({len(solution)} words): " + " → ".join(solution))
else:
    print("No valid solutions found.")