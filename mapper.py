#!/usr/bin/env python

import sys
from collections import defaultdict

def mapper():
    user_item_ratings = defaultdict(dict)

    # Read input from stdin and populate user-item ratings dictionary
    for line in sys.stdin:
        parts = line.strip().split()
        user = parts[0]
        movie = ' '.join(parts[1:-1])
        rating = parts[-1]
        user_item_ratings[user][movie] = float(rating)

    # Emit user-item ratings
    for user, item_ratings in user_item_ratings.items():
        print(f"{user}\t{item_ratings}")

if __name__ == "__main__":
    mapper()