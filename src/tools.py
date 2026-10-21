from dotenv import load_dotenv
load_dotenv()

import os
from serpapi import SerpApiClient
from typing import Dict, List

def search (query: str) -> str:
    api = SerpApiClient()
    """
    一个基于serpopi的搜索工具，
    """
