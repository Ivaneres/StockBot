from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import json


@dataclass
class SubscriptionData:
    max_price: Optional[float]


@dataclass
class Subscription:
    products: Dict[str, SubscriptionData]
