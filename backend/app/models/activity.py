from dataclasses import dataclass
from typing import Optional

@dataclass
class Activity:
    """Simple activity data structure"""
    id: str
    name: str
    activity_type: str
    date: str
    distance: Optional[float] = None  # meters
    elapsed_time: Optional[int] = None  # seconds