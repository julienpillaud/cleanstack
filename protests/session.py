from protest import ProTestSession

from protests.fixtures import get_settings
from protests.infrastructure.mongo.test_repository import mongo_repo_suite
from protests.infrastructure.sql.test_repository import sql_repo_suite

session = ProTestSession()
session.bind(get_settings)
session.add_suite(mongo_repo_suite)
session.add_suite(sql_repo_suite)
