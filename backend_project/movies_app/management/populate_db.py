import logging
import os
import sys
from sqlalchemy.orm import sessionmaker, scoped_session
import django

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set the Django settings module and initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()


# make sur to start your database and export your env variables before launching this command
# for that use script : init_test_environment or start a docker-compose up
# then use script export_db_variables

# need to import inside the function to avoid import it after the django.setup()

def populate_db(session):
    """Populate function."""
    from movies_app.models import Movie, Actor

    logging.warning("Start Populating : ")
    for i in range(100):
        logging.warning(f"Populating {i + 1} / 100")
        movie = Movie(title=f"Movie {i + 1}", description=f"Description {i + 1}")
        actor = Actor(first_name=f"First Name {i + 1}", last_name=f"Last Name {i + 1}", movie=movie)

        session.add(movie)
        session.add(actor)
        session.commit()

    logging.warning('Successfully populated the database with 100 movies and their actors.')


if __name__ == "__main__":
    from movies_app.models import engine
    _conn = engine.connect()

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        populate_db(session=db_session)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        db_session.rollback()
    finally:
        db_session.close()
