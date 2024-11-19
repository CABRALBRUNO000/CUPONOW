from datetime import datetime, timedelta
from typing import Dict, Any
import json

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, datetime] = {}
        
    def get(self, key: str) -> Any:
        if key in self._cache:
            if not self._is_expired(key):
                return self._cache[key]
            self._remove(key)
        return None
    
    def set(self, key: str, value: Any, timeout: int = 3600) -> None:
        self._cache[key] = value
        self._timestamps[key] = datetime.now() + timedelta(seconds=timeout)
    
    def _is_expired(self, key: str) -> bool:
        return datetime.now() > self._timestamps[key]
    
    def _remove(self, key: str) -> None:
        del self._cache[key]
        del self._timestamps[key]
