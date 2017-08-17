from flask import current_app
from flask_plugins import Plugin

class UHEPlugin(Plugin):
    settings_key = None

    @property
    def has_settings(self):
        """Is ``True`` if the Plugin **can** be installed."""
        if self.settings_key is not None:
            return True
        return False
 
    @property
    def installed(self):
        is_installed = False
        if self.has_settings:
            group = SettingsGroup.query.\
                filter_by(key=self.settings_key).\
                first()
            is_installed = group and len(group.settings.all()) > 0
        return is_installed

    def register_blueprint(self, blueprint, **kwargs):
        """Registers a blueprint.
        :param blueprint: The blueprint which should be registered.
        """
        current_app.register_blueprint(blueprint, **kwargs)