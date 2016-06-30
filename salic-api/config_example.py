#Application version
VERSION = "0.2.2"

# API version
BASE_VERSION = 'alpha'

SALIC_BASE_URL = 'http://novosalic.cultura.gov.br/'

# Webserver
WEBSERVER_PORT = 8000
WEBSERVER_ADDR = '0.0.0.0'
SUBPROCESS_NUMBER = 10

# for Swagger documentation providing
SWAGGER_DEF_PATH = 'swagger_specification_PT-BR.json'

# Pagination
LIMIT_PAGING = 100
OFFSET_PAGING = 0

# Return content types
AVAILABLE_CONTENT_TYPES = ('application/xml', 'application/json', 'text/csv')

# DATABASE
DATABASE_HOST = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_NAME = 'sac'

# Rate limiting
RATE_LIMITING_ACTIVE = False
GLOBAL_RATE_LIMITS =  "1000 per day"

#LOGGING
LOGFILE = '/opt/salic/salic-api/log/salic_api.log'
LEVELOFLOG = 'DEBUG'
STREAMTYPE = 'FILE'
