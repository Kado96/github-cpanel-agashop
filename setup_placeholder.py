import shutil
import os

src = r"C:\Users\Donald\.gemini\antigravity\brain\4c9ae2af-12ab-4506-afbd-9ae70c1fe8bf\placeholder_1779180948222.png"
dst = r"e:\AgaShop\github-cpanel-agashop\frontend\public\placeholder.png"

if os.path.exists(src):
    shutil.copy(src, dst)
    print("Success: Placeholder copied to frontend/public/placeholder.png")
else:
    # If the source file was moved or is inaccessible, write a minimal base64 fallback PNG
    import base64
    # Minimal 1x1 grey PNG base64
    fallback_png = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
    with open(dst, "wb") as f:
        f.write(base64.b64decode(fallback_png))
    print("Success: Written fallback 1x1 PNG to frontend/public/placeholder.png")
