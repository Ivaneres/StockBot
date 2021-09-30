from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Subscription:
    memberID: str
    subscribed_categories: List[Dict] # example: [{"category":"RTX3090", "max price": 1500},{...}]