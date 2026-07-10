from apte import ApteSession

from tests_apte.fixtures import get_settings
from tests_apte.infrastructure.mongo.test_repository import mongo_repo_suite
from tests_apte.infrastructure.sql.test_repository import sql_repo_suite

session = ApteSession()
session.bind(get_settings)
session.add_suite(mongo_repo_suite)
session.add_suite(sql_repo_suite)
