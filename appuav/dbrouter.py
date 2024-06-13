class DbRouter:
    """A router to control all database operations on models."""

    def db_for_read(self, model, **hints):
        """Attempts to read db1 data."""
        if model._meta.app_label == "lcmed":
            return "lcmed"
        return "default"

    def db_for_write(self, model, **hints):
        """Attempts to write db2 data."""
        if model._meta.app_label == "lcmed":
            return "lcmed"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps with different databases."""
        db_list = ("default", "lcmed")
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure the app only appears in the 'db1' database."""
        if app_label == "lcmed":
            return db == "lcmed"
        return "default"
