from flaskblog import db
from flask import current_app


class ModelMixin:
    def save_to_db(self) -> None:
        """
        Save the current instance to the database.
        """
        with current_app.app_context():
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete the current instance from the database.
        """
        db.session.delete(self)
        db.session.commit()
