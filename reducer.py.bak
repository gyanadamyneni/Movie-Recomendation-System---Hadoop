#!/usr/bin/env python

import sys
from collections import defaultdict

def calculate_mean(ratings):
    return sum(ratings) / len(ratings)

def calculate_pearson_correlation(user_ratings, other_user_ratings):
    common_movies = set(user_ratings.keys()) & set(other_user_ratings.keys())
    if not common_movies:
        return 0  # No common movies, return correlation coefficient as 0

    # Calculating the means of ratings for both users
    user_mean = calculate_mean(user_ratings.values())
    other_user_mean = calculate_mean(other_user_ratings.values())

    # Calculating numerator and denominators for Pearson correlation coefficient
    numerator = sum((user_ratings[movie] - user_mean) * (other_user_ratings[movie] - other_user_mean) for movie in common_movies)
    denominator_user = sum((rating - user_mean) ** 2 for rating in user_ratings.values())
    denominator_other_user = sum((rating - other_user_mean) ** 2 for rating in other_user_ratings.values())

    # Calculating Pearson correlation coefficient
    if denominator_user == 0 or denominator_other_user == 0:
        return 0  # Handle division by zero
    return numerator / (denominator_user ** 0.5 * denominator_other_user ** 0.5)

def generate_recommendations(user, user_item_ratings):
    # Selecting the top-rated movies by the user
    top_rated_movies = sorted(user_item_ratings[user], key=user_item_ratings[user].get, reverse=True)[:5]

    # Collecting ratings from other users who rated the same movies
    similar_users_ratings = defaultdict(float)
    for movie in top_rated_movies:
        for other_user in user_item_ratings:
            if other_user != user and movie in user_item_ratings[other_user]:
                similar_users_ratings[other_user] += user_item_ratings[other_user][movie]

    # Calculating the Pearson correlation coefficient for each user
    pearson_correlations = {other_user: calculate_pearson_correlation(user_item_ratings[user], user_item_ratings[other_user])
                            for other_user in similar_users_ratings}

    # Filtering out users with non-positive Pearson correlation coefficient
    positive_correlation_users = {other_user: pearson for other_user, pearson in pearson_correlations.items() if pearson > 0}

    # Sorting users by Pearson correlation coefficient and return recommendations
    sorted_similar_users = sorted(positive_correlation_users.items(), key=lambda x: x[1], reverse=True)[:5]
    recommendations = set()  # Using a set to avoid recommending the same movie multiple times
    for other_user, _ in sorted_similar_users:
        for movie in user_item_ratings[other_user]:
            if movie not in user_item_ratings[user]:
                recommendations.add(movie)
    return list(recommendations)[:5]

def reducer():
    # Initializing a dictionary to store user-item ratings
    user_item_ratings = defaultdict(dict)

    # Reading input from mapper and populate user-item ratings dictionary
    for line in sys.stdin:
        parts = line.strip().split("\t")
        user = parts[0]
        rating_str = parts[1][1:-1]  # Remove the braces {}
        if rating_str:  # Check if there are ratings
            ratings = rating_str.split(", ")
            for rating in ratings:
                movie, rating = rating.split(": ")
                user_item_ratings[user][movie] = float(rating)

    # Generating movie recommendations for each user
    for user in user_item_ratings:
        recommendations = generate_recommendations(user, user_item_ratings)
        print(f"{user}\t{recommendations}")

if __name__ == "__main__":
    reducer()