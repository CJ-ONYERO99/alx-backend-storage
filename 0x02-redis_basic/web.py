#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracker
"""

import redis
from typing import Callable
from functools import wraps
import requests

def request_count(func: Callable) -> Callable:
    '''Request count for a requested url'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        redis_client = redis.Redis()
        url = args[0]
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"
        
        # Increment the count
        redis_client.incr(count_key)
        
        # Check if the result is cached
        if redis_client.get(cache_key) is not None:
            return redis_client.get(cache_key).decode('utf-8')
        
        # If not cached, call the function and cache the result
        result = func(*args, **kwargs)
        redis_client.setex(cache_key, 10, result)
        return result
    return wrapper


@request_count
def get_page(url: str) -> str:
    '''Uses the requests module to obtain the HTML content of a particular URL and returns it'''
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    print(get_page('https://httpbin.org/anything'))
    print(get_page('http://slowwly.robertomurray.co.uk'))
    print(get_page('http://google.com'))
