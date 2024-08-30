#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracker
"""

import redis
from typing import Callable
from functools import wraps
import requests


def request_count(func: Callable) -> Callable:
  @wraps(func)
  def wrapper(*args, **kwargs):
    redis_client = redis.Redis()
    url = args[0]
    key = f"count:{url}"
    
    # Reset count to 0 before incrementing on each request
    redis_client.set(key, 0, ex=10)
    redis_client.incr(key)
    return func(*args, **kwargs)
  return wrapper


@request_count
def get_page(url: str) -> str:
  '''Uses the requests module to obtain the HTML
  content of a particular URL and returns it'''
  response = requests.get(url)
  return response.text


if __name__ == '__main__':
  print(get_page('https://httpbin.org/anything'))
  print(get_page('http://slowwly.robertomurray.co.uk'))
  print(get_page('http://google.com'))
