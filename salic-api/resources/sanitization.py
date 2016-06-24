from format_utils import truncate, remove_blanks, remove_html_tags, HTMLEntitiesToUnicode



def sanitize(value, truncated = True, keep_markup = False):

    if value is None:
        return u""

    if not keep_markup:
        value = remove_html_tags(value)
        value = HTMLEntitiesToUnicode(value)

    if truncated:
        value = truncate(value)

    return value
