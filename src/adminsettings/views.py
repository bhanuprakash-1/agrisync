from .mixins import SettingsMixin


class SettingsChangeView(SettingsMixin):
    """
    View for settings change
    """
    pass


class SettingsChangeDoneView(SettingsMixin):
    """
    change settings and redirect to change settings
    """
    pass


class SettingsResetView(SettingsMixin):
    """
    reset settings and redirect to change settings
    """
    pass
