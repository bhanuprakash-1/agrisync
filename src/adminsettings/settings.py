from .fields import BooleanSettingsField


class Settings(object):
    """
    settings that can be changed by admin panel
    Make sure settings is in upper case
    """

    DEBUG = BooleanSettingsField('DEBUG', verbous_name='Debug')
    MAINTENANCE_MODE = BooleanSettingsField('MAINTENANCE_MODE',  verbous_name='Maintenance Mode')
    MAIN_APP_MAINTENANCE = BooleanSettingsField('MAIN_APP_MAINTENANCE',  verbous_name='Main app maintenance')
    OAUTH_APP_MAINTENANCE = BooleanSettingsField('OAUTH_APP_MAINTENANCE', verbous_name='Oauth app maintenance')
    FORUM_APP_MAINTENANCE = BooleanSettingsField('FORUM_APP_MAINTENANCE', verbous_name='Forum app maintenance')


allsettings = Settings()
