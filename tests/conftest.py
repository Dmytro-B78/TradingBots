import os
import shutil
import stat

# Сохраняем оригинал
_ORIG_OS_REPLACE = os.replace

def _ensure_writable(path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    try:
        attrs = os.stat(path).st_mode
        if attrs & stat.S_IREAD:
            os.chmod(path, stat.S_IWRITE)
    except FileNotFoundError:
        pass

def _safe_replace(src: str, dst: str):
    # Если цель — data/whitelist.json, перенаправляем на WHITELIST_PATH
    if os.path.normpath(dst).endswith(os.path.normpath("data/whitelist.json")):
        dst = os.getenv("WHITELIST_PATH", os.path.join(os.getenv("TEMP", "/tmp"), "whitelist_test.json"))
    try:
        return _ORIG_OS_REPLACE(src, dst)
    except PermissionError:
        _ensure_writable(dst)
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except Exception:
            pass
        with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
            shutil.copyfileobj(fsrc, fdst, length=1024 * 1024)
        return None

# Переопределяем глобально
os.replace = _safe_replace
