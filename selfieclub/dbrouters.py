class BaseDbRouter(object):
    # (TODO: pt-79657238) # pylint: disable=protected-access, no-member
    def db_for_read(self, model, **hints):
        # 'hints' is required
        # pylint: disable=unused-argument
        if self.is_managed_app(model._meta.app_label):
            return self.__class__.CONFIG_NAME
        return None

    def db_for_write(self, model, **hints):
        # 'hints' is required
        # pylint: disable=unused-argument
        if self.is_managed_app(model._meta.app_label):
            return self.__class__.CONFIG_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # 'hints' is required
        # pylint: disable=unused-argument
        """
        Allow relations if both models are in the same DB
        """
        if obj1._state.db == self.__class__.CONFIG_NAME \
                and obj2._state.db == self.__class__.CONFIG_NAME:
            return True
        return None

    def allow_syncdb(self, current_db, model):
        if current_db == self.__class__.CONFIG_NAME \
                and self.is_managed_app(model._meta.app_label):
            return True
        elif self.is_managed_app(model._meta.app_label):
            return False
        return None

    def is_managed_app(self, label):
        return label in self.__class__.APP_LABELS


class SelfieClubDbRouter(BaseDbRouter):
    CONFIG_NAME = 'selfieclub'
    APP_LABELS = (
        'media',
        'newsfeed_member',
        'messaging',
        'member',
        'club',
        'status',
    )


class DjangoDbRouter(BaseDbRouter):
    # (TODO: pt-79657238) # pylint: disable=protected-access
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
        if self.is_managed_app(obj1._meta.app_label) \
                or self.is_managed_app(obj2._meta.app_label):
            return True
        return None


class FailDbRouter(object):
    # noqa (TODO: pt-79657238) # pylint: disable=protected-access, abstract-class-not-used
    def db_for_read(self, model, **hints):
        # pylint: disable=unused-argument, no-self-use
        raise Exception(
            "Unknown application '{}'".format(model._meta.app_label))

    def db_for_write(self, model, **hints):
        # pylint: disable=unused-argument, no-self-use
        raise Exception(
            "Unknown application '{}'".format(model._meta.app_label))

    def allow_relation(self, obj1, obj2, **hints):
        # pylint: disable=unused-argument, no-self-use
        raise Exception("Unknown relationship")

    def allow_syncdb(self, current_db, model):
        # pylint: disable=unused-argument, no-self-use
        raise Exception(
            "Unknown application '{}' while updating '{}'"
            .format(model._meta.app_label, current_db))
