from datetime import datetime, timedelta
from typing import Dict, List


class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = {}
        self.max_requests = 10  # per hour
        self.window = timedelta(hours=1)

    def is_allowed(self, ip: str) -> tuple[bool, int]:
        """Check if request is allowed. Returns (allowed, minutes_until_reset)"""
        now = datetime.now()

        # Clean old requests
        if ip in self.requests:
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if now - req_time < self.window
            ]
        else:
            self.requests[ip] = []

        # Check limit
        if len(self.requests[ip]) >= self.max_requests:
            oldest = min(self.requests[ip])
            reset_time = oldest + self.window
            minutes_left = int((reset_time - now).total_seconds() / 60)
            return False, minutes_left

        # Allow request
        self.requests[ip].append(now)
        return True, 0

    def cleanup(self):
        """Remove old IPs from memory"""
        now = datetime.now()
        self.requests = {
            ip: times for ip, times in self.requests.items()
            if any(now - t < self.window for t in times)
        }


rate_limiter = RateLimiter()
