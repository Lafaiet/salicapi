
from app import app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.ext.limiter import HEADERS
from config import GLOBAL_RATE_LIMITS, RATE_LIMITING_ACTIVE





limiter = Limiter(
    app,
    key_func=get_remote_address,
    headers_enabled = True,
)


limiter.header_mapping = {
    HEADERS.LIMIT : "X-My-Limit",
    HEADERS.RESET : "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"
}

shared_limiter = limiter.shared_limit(GLOBAL_RATE_LIMITS, scope="salic_api")
