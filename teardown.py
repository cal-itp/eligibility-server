from flask_sqlalchemy import inspect
from eligibility_server import app
import logging


logger = logging.getLogger("teardown")

if __name__ == "__main__":
    inspector = inspect(app.db.engine)

    if inspector.get_table_names():
        logger.info(f"Users to be deleted: {app.User.query.count()}")
        app.User.query.delete()
        app.db.session.commit()
        app.db.drop_all()
        logger.info("Database dropped.")
    else:
        logger.info("Database does not exist.")
