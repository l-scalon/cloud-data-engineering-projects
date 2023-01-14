from variables import Variable as env
from database.execute import File
import logging

logger = logging.getLogger('redshift')
logging.basicConfig(level = logging.INFO)

class Redshift:

    def __init__(self) -> None:
        pass

    def unload(self, connection):
        unload_file = env().path(dir = 'sql', file = 'unload.sql')
        File().execute(connection = connection, file = unload_file)
        logger.info("Unload done.")

    def create_external_schema(self, connection):
        external_schema_file = env().path(dir = 'sql', file = 'external_schema.sql')
        File().execute(connection = connection, file = external_schema_file)
        logger.info("Creating external schema done.")

    def create_views(self, connection):
        create_views_file = env().path(dir = 'sql', file = 'create_views.sql')
        File().execute(connection = connection, file = create_views_file)
        logger.info("Creating views done.")