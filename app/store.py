from threading import Lock
from app.models import ComicResult


class ComicStore:
    def __init__(self) -> None:
        self._items: dict[str, ComicResult] = {}
        self._lock = Lock()

    def put(self, comic: ComicResult) -> None:
        with self._lock:
            self._items[comic.comic_id] = comic

    def get(self, comic_id: str) -> ComicResult | None:
        with self._lock:
            return self._items.get(comic_id)


store = ComicStore()
