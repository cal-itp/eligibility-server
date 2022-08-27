import logging

from flask_sqlalchemy import inspect

from eligibility_server.app import app
from eligibility_server.database import db, User

logger = logging.getLogger("teardown")

if __name__ == "__main__":
    with app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            try:
                logger.info(f"Users to be deleted: {User.query.count()}")
                User.query.delete()
                db.session.commit()
            except Exception as e:
                logger.warning("Failed to query for Users", e)

            db.drop_all()
            logger.info("Database dropped.")
        else:
            logger.info("Database does not exist.")
