from protest import ProTestSession

from protests.factories.items import item
from protests.fixtures import settings
from protests.infrastructure.mongo.test_repository import mongo_repo_suite

session = ProTestSession()
session.bind(settings)
session.bind(item)
session.add_suite(mongo_repo_suite)
