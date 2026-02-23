# Rock Paper Scissors AI

An intelligent Rock Paper Scissors bot that defeats multiple opponents with different strategies, winning at least 60% of games against each.

## Strategies Implemented

- **Pattern Recognition**: Detects and exploits patterns in opponent play
- **Opponent Identification**: Automatically identifies which bot it's playing against
- **Adaptive Play**: Uses different strategies for different opponents
- **Frequency Analysis**: Tracks move frequencies to predict future plays

## How It Works

The bot analyzes the opponent's move history and selects the optimal counter-strategy:
- **Quincy**: Predicts and counters Quincy's fixed pattern
- **Kris**: Anticipates Kris's reactive strategy
- **Mrugesh**: Counters Mrugesh's frequency-based approach
- **Abbey**: Uses pattern detection to outsmart Abbey's predictive algorithm
- **Unknown**: Falls back to general pattern recognition

## Requirements

- Python 3.6+
- NumPy

## Usage

```python
from RPS_game import play, quincy
from RPS import player

# Test against Quincy
play(player, quincy, 1000, verbose=True)
