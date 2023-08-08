#!/usr/bin/python3

""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
""

import json
import requests

def count_words(subreddit, word_list, after=None, word_count=None):
    if word_count is None:
        word_count = {}

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot/.json?after={after}"

    headers = {
        "User-Agent": "MyRedditBot/1.0"
    }

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 404:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])
    
    for post in posts:
        title = post.get("data", {}).get("title", "").lower()
        for keyword in word_list:
            if keyword.lower() in title:
                if keyword in word_count:
                    word_count[keyword] += 1
                else:
                    word_count[keyword] = 1

    after = data.get("after")
    if after is not None:
        count_words(subreddit, word_list, after, word_count)
    else:
        sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
        for keyword, count in sorted_counts:
            print(f"{keyword}: {count}")
