from .settings import allsettings
from .admin import adminsettings
from .utils import save_default, load_settings

__all__ = ('allsettings', 'adminsettings')


save_default()
load_settings()
