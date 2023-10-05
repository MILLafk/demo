"""
ASGI config for video_process project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "video_process"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_process.settings")

application = get_asgi_application()
