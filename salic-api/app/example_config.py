#Application version
VERSION = "0.0.2"

# API version
BASE_VERSION = 'beta'

SALIC_BASE_URL = 'http://novosalic.cultura.gov.br/'
API_ROOT_URL = 'http://vm-debian:8000/%s/'%BASE_VERSION

URL_KEY = ''

# Webserver
WEBSERVER_PORT = 8000
WEBSERVER_ADDR = '0.0.0.0'
SUBPROCESS_NUMBER = 10

# for Swagger documentation providing
SWAGGER_DEF_PATH = '/home/debian/salicapi/swagger_specification_PT-BR.json'

# Pagination
LIMIT_PAGING = 100
OFFSET_PAGING = 0

# Caching
CACHING_ACTIVE = False
CACHE_TYPE = 'redis'
GLOBAL_CACHE_TIMEOUT = 500
CACHE_REDIS_URL = 'redis://localhost:6379'

# Return content types
AVAILABLE_CONTENT_TYPES = ('application/xml', 'application/json', 'text/csv')


SQL_DRIVER = 'pymssql'
DATABASE_HOST = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_NAME = ''
DATABASE_PORT = '1433'

# Rate limiting
RATE_LIMITING_ACTIVE = False
GLOBAL_RATE_LIMITS =  "1000 per day"

#LOGGING
LOGFILE = '/opt/salic/salic-api/log/salic_api.log'
LEVELOFLOG = 'DEBUG'
STREAMTYPE = 'SCREEN'
