# recommendation_logic.py
# Author: Anand Gopal Yadav
# Description: Social Media Recommendation System (Pure Python)
# Data file: data/massive_data.json

import json
import os

# --------------------------------------------------
# Load Data (SAFE PATH)
# --------------------------------------------------
def load_data(filename="massive_data.json"):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "data", filename)

    with open(file_path, "r") as f:
        return json.load(f)


# --------------------------------------------------
# Data Cleaning
# --------------------------------------------------
def data_clean(data):
    # Remove users with blank names
    data["users"] = [
        user for user in data["users"] if user["name"].strip()
    ]

    # Remove duplicate friends
    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))

    # Remove inactive users
    data["users"] = [
        user for user in data["users"]
        if user["friends"] or user["liked_pages"]
    ]

    # Remove duplicate pages
    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    return data


# --------------------------------------------------
# Helper Functions (ID → Name)
# --------------------------------------------------
def get_user_name(user_id, data):
    for user in data["users"]:
        if user["id"] == user_id:
            return user["name"]
    return "Unknown User"


def get_page_name(page_id, data):
    for page in data["pages"]:
        if page["id"] == page_id:
            return page["name"]
    return "Unknown Page"


# --------------------------------------------------
# Friend Recommendation Logic (WITH SCORE)
# --------------------------------------------------
def find_people_you_may_know(user_id, data):
    user_friends = {
        user["id"]: set(user["friends"])
        for user in data["users"]
    }

    if user_id not in user_friends:
        return []

    direct_friends = user_friends[user_id]
    suggestions = {}

    for friend in direct_friends:
        for mutual in user_friends.get(friend, []):
            if mutual != user_id and mutual not in direct_friends:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    return sorted(
        [(uid, score) for uid, score in suggestions.items() if score >= 1],
        key=lambda x: x[1],
        reverse=True
    )


# --------------------------------------------------
# Page Recommendation Logic (WITH SCORE)
# --------------------------------------------------
def find_pages_you_might_like(user_id, data):
    user_pages = {
        user["id"]: set(user["liked_pages"])
        for user in data["users"]
    }

    if user_id not in user_pages:
        return []

    user_liked_pages = user_pages[user_id]
    page_scores = {}

    for other_user, pages in user_pages.items():
        if other_user == user_id:
            continue

        shared_pages = user_liked_pages.intersection(pages)

        if len(shared_pages) >= 1:
            for page in pages:
                if page not in user_liked_pages:
                    page_scores[page] = page_scores.get(page, 0) + len(shared_pages)

    return sorted(
        [(pid, score) for pid, score in page_scores.items() if score >= 1],
        key=lambda x: x[1],
        reverse=True
    )


# --------------------------------------------------
# FINAL OUTPUT (ID = NAME + SCORE)
# --------------------------------------------------
def friend_suggestions_with_names(user_id, data):
    results = find_people_you_may_know(user_id, data)
    return [
        {
            "id": uid,
            "name": get_user_name(uid, data),
            "score": score
        }
        for uid, score in results
    ]


def page_suggestions_with_names(user_id, data):
    results = find_pages_you_might_like(user_id, data)
    return [
        {
            "id": pid,
            "name": get_page_name(pid, data),
            "score": score
        }
        for pid, score in results
    ]


# --------------------------------------------------
# TEST (RUN DIRECTLY)
# --------------------------------------------------
if __name__ == "__main__":
    data = load_data()
    data = data_clean(data)

    print("Friend Suggestions:")
    for f in friend_suggestions_with_names(2, data):
        print(f)

    print("\nPage Suggestions:")
    for p in page_suggestions_with_names(3, data):
        print(p)


# # recommendation_logic.py
# # Author: Anand Gopal Yadav
# # Description: Social Media Recommendation System (Pure Python)
# # Data file: data/massive_data.json

# import json
# import os

# # --------------------------------------------------
# # Load Data (SAFE PATH)
# # --------------------------------------------------
# def load_data(filename="massive_data.json"):
#     base_dir = os.path.dirname(__file__)
#     file_path = os.path.join(base_dir, "data", filename)

#     with open(file_path, "r") as f:
#         return json.load(f)


# # --------------------------------------------------
# # Data Cleaning
# # --------------------------------------------------
# def data_clean(data):
#     # Remove users with blank names
#     data["users"] = [
#         user for user in data["users"] if user["name"].strip()
#     ]

#     # Remove duplicate friends
#     for user in data["users"]:
#         user["friends"] = list(set(user["friends"]))

#     # Remove inactive users
#     data["users"] = [
#         user for user in data["users"]
#         if user["friends"] or user["liked_pages"]
#     ]

#     # Remove duplicate pages
#     unique_pages = {}
#     for page in data["pages"]:
#         unique_pages[page["id"]] = page
#     data["pages"] = list(unique_pages.values())

#     return data


# # --------------------------------------------------
# # Helper Functions (ID → Name)
# # --------------------------------------------------
# def get_user_name(user_id, data):
#     for user in data["users"]:
#         if user["id"] == user_id:
#             return user["name"]
#     return "Unknown User"


# def get_page_name(page_id, data):
#     for page in data["pages"]:
#         if page["id"] == page_id:
#             return page["name"]
#     return "Unknown Page"


# # --------------------------------------------------
# # Friend Recommendation Logic
# # --------------------------------------------------
# def find_people_you_may_know(user_id, data):
#     user_friends = {}

#     for user in data["users"]:
#         user_friends[user["id"]] = set(user["friends"])

#     if user_id not in user_friends:
#         return []

#     direct_friends = user_friends[user_id]
#     suggestions = {}

#     for friend in direct_friends:
#         for mutual in user_friends.get(friend, []):
#             if mutual != user_id and mutual not in direct_friends:
#                 suggestions[mutual] = suggestions.get(mutual, 0) + 1

#     sorted_suggestions = sorted(
#         suggestions.items(),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return [uid for uid, _ in sorted_suggestions]


# # --------------------------------------------------
# # Page Recommendation Logic
# # --------------------------------------------------
# def find_pages_you_might_like(user_id, data):
#     user_pages = {}

#     for user in data["users"]:
#         user_pages[user["id"]] = set(user["liked_pages"])

#     if user_id not in user_pages:
#         return []

#     user_liked_pages = user_pages[user_id]
#     page_scores = {}

#     for other_user, pages in user_pages.items():
#         if other_user == user_id:
#             continue

#         shared_pages = user_liked_pages.intersection(pages)

#         for page in pages:
#             if page not in user_liked_pages:
#                 page_scores[page] = page_scores.get(page, 0) + len(shared_pages)

#     sorted_pages = sorted(
#         page_scores.items(),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return [pid for pid, _ in sorted_pages]


# # --------------------------------------------------
# # FINAL OUTPUT (ID = NAME)
# # --------------------------------------------------
# def friend_suggestions_with_names(user_id, data):
#     friend_ids = find_people_you_may_know(user_id, data)
#     return [f"{fid} = {get_user_name(fid, data)}" for fid in friend_ids]


# def page_suggestions_with_names(user_id, data):
#     page_ids = find_pages_you_might_like(user_id, data)
#     return [f"{pid} = {get_page_name(pid, data)}" for pid in page_ids]


# # --------------------------------------------------
# # TEST (RUN DIRECTLY)
# # --------------------------------------------------
# if __name__ == "__main__":
#     data = load_data()
#     data = data_clean(data)

#     print("Friend Suggestions:")
#     print(friend_suggestions_with_names(2, data))

#     print("\nPage Suggestions:")
#     print(page_suggestions_with_names(3, data))
