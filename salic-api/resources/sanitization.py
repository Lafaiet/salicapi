from format_utils import truncate, remove_blanks, remove_html_tags, HTMLEntitiesToUnicode
import re



def sanitize(value, truncated = True, keep_markup = False):

    if value is None:
        return u""

    if not keep_markup:
        value = remove_html_tags(value)
        value = HTMLEntitiesToUnicode(value)

    if truncated:
        value = truncate(value)

    # Removing tabs, newlines and other "whitespace-like" characters.
    value  = re.sub( '\s+', ' ', value ).strip()

    return value
