class BaseDbRouter(object):
    def db_for_read(self, model, **hints):
        if self.isManagedApp(model._meta.app_label):
            return self.__class__.CONFIG_NAME
        return None

    def db_for_write(self, model, **hints):
        if self.isManagedApp(model._meta.app_label):
            return self.__class__.CONFIG_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the same DB
        """
        if obj1._state.db == self.__class__.CONFIG_NAME \
                and obj2._state.db == self.__class__.CONFIG_NAME:
            return True
        return None

    def allow_syncdb(self, current_db, model):
        if current_db == self.__class__.CONFIG_NAME \
                and self.isManagedApp(model._meta.app_label):
            return True
        elif self.isManagedApp(model._meta.app_label):
            return False
        return None

    def isManagedApp(self, label):
        return label in self.__class__.APP_LABELS


class SelfieClubDbRouter(BaseDbRouter):
    CONFIG_NAME = 'selfieclub'
    APP_LABELS = (
        'media',
        'newsfeed_user',
        'member',
        'club',
        'selfie',
    )


class DjangoDbRouter(BaseDbRouter):
    CONFIG_NAME = 'django'
    APP_LABELS = (
        'admin',
        'auth',
        'contenttypes',
        'sessions'
    )

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if self.isManagedApp(obj1._meta.app_label) \
                or self.isManagedApp(obj2._meta.app_label):
            return True
        return None


class FailDbRouter(object):
    def db_for_read(self, model, **hints):
        raise NotImplementedError("Unknown application '{}'".format(model._meta.app_label))

    def db_for_write(self, model, **hints):
        raise NotImplementedError("Unknown application '{}'".format(model._meta.app_label))

    def allow_relation(self, obj1, obj2, **hints):
        raise NotImplementedError("Unknown relationship")

    def allow_syncdb(self, current_db, model):
        raise NotImplementedError(
            "Unknown application '{}' while updating '{}'"
            .format(model._meta.app_label, current_db))
