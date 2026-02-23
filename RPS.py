import random
import numpy as np
from collections import Counter, defaultdict

# Global variables to track state across function calls
opponent_patterns = {}
opponent_strategies = {}
opponent_history_dict = {}
pattern_length = 4  # Length of patterns to track

def player(prev_play, opponent_history=[]):
    """
    Main player function that uses different strategies based on opponent behavior
    """
    global opponent_patterns, opponent_strategies, opponent_history_dict
    
    # Initialize on first move
    if prev_play == '':
        opponent_history.clear()
        # Reset global state for new match
        opponent_patterns = {}
        opponent_strategies = {}
        opponent_history_dict = {}
        return random.choice(['R', 'P', 'S'])
    
    # Add opponent's last move to history
    opponent_history.append(prev_play)
    
    # Identify which opponent we're playing against
    opponent_id = identify_opponent(opponent_history)
    
    # Choose strategy based on identified opponent
    if opponent_id == 'quincy':
        return beat_quincy(opponent_history)
    elif opponent_id == 'mrugesh':
        return beat_mrugesh(opponent_history)
    elif opponent_id == 'abbey':
        return beat_abbey(opponent_history)
    elif opponent_id == 'kris':
        return beat_kris(opponent_history)
    else:
        # Default strategy for unknown opponents
        return beat_unknown(opponent_history)

def identify_opponent(history):
    """
    Identify which bot we're playing against based on their patterns
    """
    if len(history) < 10:
        return 'unknown'
    
    # Check for Quincy's pattern (repeats every 5 moves: R,P,S,R,P)
    if len(history) >= 5:
        quincy_pattern = ['R', 'P', 'S', 'R', 'P']
        matches = 0
        for i in range(min(5, len(history))):
            if history[i] == quincy_pattern[i % 5]:
                matches += 1
        if matches >= 4:
            return 'quincy'
    
    # Check for Kris (always beats your last move)
    if len(history) >= 3:
        kris_pattern = True
        for i in range(1, len(history)):
            expected = beat_move(get_counter_move(history[i-1]))
            if history[i] != expected:
                kris_pattern = False
                break
        if kris_pattern and len(history) > 5:
            return 'kris'
    
    # Check for Mrugesh (uses frequency analysis)
    # This is harder to identify, so we'll use a fallback
    
    # Check for Abbey (looks for patterns in your play)
    # Also hard to identify precisely
    
    return 'unknown'

def beat_move(move):
    """Returns the move that beats the given move"""
    if move == 'R':
        return 'P'
    elif move == 'P':
        return 'S'
    else:  # move == 'S'
        return 'R'

def get_counter_move(move):
    """Returns the move that would lose to the given move (for pattern detection)"""
    if move == 'R':
        return 'S'
    elif move == 'P':
        return 'R'
    else:  # move == 'S'
        return 'P'

def beat_quincy(history):
    """
    Quincy plays in a pattern: R, P, S, R, P (repeats every 5)
    To beat Quincy, play the counter to his next move
    """
    quincy_pattern = ['R', 'P', 'S', 'R', 'P']
    next_index = len(history) % 5
    quincy_next = quincy_pattern[next_index]
    return beat_move(quincy_next)

def beat_kris(history):
    """
    Kris always plays the move that beats your last move
    If you played R last, Kris plays P
    So to beat Kris, play the move that would lose to your last move
    """
    if not history:
        return random.choice(['R', 'P', 'S'])
    
    my_last_move = history[-1]  # This is actually opponent's move from our perspective
    # Wait, careful: history stores opponent's moves
    # For Kris, we need to know what WE played last
    
    # Since we don't have direct access to our own history,
    # we need to infer it from opponent's moves
    if len(history) >= 2:
        # Kris's move at time t is based on our move at time t-1
        # So our move at time t-1 is the counter to Kris's move at time t-1
        our_last_move = get_counter_move(history[-1])
        # Kris will play the beat of our_last_move
        kris_next = beat_move(our_last_move)
        # We want to beat kris_next
        return beat_move(kris_next)
    
    return random.choice(['R', 'P', 'S'])

def beat_mrugesh(history):
    """
    Mrugesh looks at your last 10 moves, finds the most frequent,
    and plays the counter to that move
    """
    if len(history) < 3:
        return random.choice(['R', 'P', 'S'])
    
    # Look at last min(10, len(history)) moves
    recent = history[-10:] if len(history) >= 10 else history
    
    # Find most frequent move in opponent's history
    counter = Counter(recent)
    most_common = counter.most_common(1)[0][0]
    
    # Mrugesh will play the beat of most_common
    mrugesh_play = beat_move(most_common)
    
    # We want to beat mrugesh_play
    return beat_move(mrugesh_play)

def beat_abbey(history):
    """
    Abbey looks for patterns of length 2 in your play
    She predicts your next move based on your last move and the most common follow-up
    """
    if len(history) < 3:
        return random.choice(['R', 'P', 'S'])
    
    # Build pattern dictionary of opponent's moves
    patterns = {}
    for i in range(len(history) - 1):
        pattern = history[i] + history[i + 1]
        if pattern not in patterns:
            patterns[pattern] = []
        if i + 2 < len(history):
            patterns[pattern].append(history[i + 2])
    
    # Get last two opponent moves
    last_two = history[-2] + history[-1] if len(history) >= 2 else history[-1]
    
    # Predict opponent's next move based on patterns
    if last_two in patterns and patterns[last_two]:
        predicted = Counter(patterns[last_two]).most_common(1)[0][0]
    else:
        # Fallback to frequency analysis
        predicted = Counter(history[-5:]).most_common(1)[0][0] if history else 'R'
    
    # Abbey will try to beat our predicted move
    # So we should play the move that would lose to Abbey's counter
    abbey_play = beat_move(predicted)
    return beat_move(abbey_play)

def beat_unknown(history):
    """
    General strategy for unknown opponents:
    Use pattern recognition and frequency analysis
    """
    if len(history) < 5:
        return random.choice(['R', 'P', 'S'])
    
    # Try to detect patterns of length 3
    patterns = []
    for length in [3, 4]:
        if len(history) >= length:
            recent = ''.join(history[-length:])
            for i in range(len(history) - length):
                if ''.join(history[i:i+length]) == recent:
                    if i + length < len(history):
                        patterns.append(history[i+length])
    
    if patterns:
        # Predict next move based on found patterns
        predicted = Counter(patterns).most_common(1)[0][0]
        return beat_move(predicted)
    
    # If no patterns found, use frequency analysis of last 10 moves
    recent = history[-10:]
    counter = Counter(recent)
    most_common = counter.most_common(1)[0][0]
    return beat_move(most_common)
