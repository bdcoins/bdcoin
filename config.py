# config.py
import os

PORT = int(os.environ.get("PORT", 5000))
INITIAL_REWARD = 50
INITIAL_DIFFICULTY = 4 

# Difficulty Adjustment Settings
TARGET_BLOCK_TIME = 60  # Goal: 1 block every 60 seconds
ADJUSTMENT_INTERVAL = 5 # Adjust difficulty every 5 blocks
