from RPS_game import play, quincy, mrugesh, abbey, kris
from RPS import player
import random

# Test against each opponent
print("Testing against Quincy...")
play(player, quincy, 1000, verbose=True)

print("\nTesting against Mrugesh...")
play(player, mrugesh, 1000, verbose=True)

print("\nTesting against Abbey...")
play(player, abbey, 1000, verbose=True)

print("\nTesting against Kris...")
play(player, kris, 1000, verbose=True)

# Test all at once with less verbose output
def test_all():
    opponents = [quincy, mrugesh, abbey, kris]
    opponent_names = ["Quincy", "Mrugesh", "Abbey", "Kris"]
    
    for opponent, name in zip(opponents, opponent_names):
        print(f"\nPlaying 100 games against {name}:")
        play(player, opponent, 100, verbose=False)

if __name__ == "__main__":
    test_all()
