from ..format_utils import truncate, remove_blanks, remove_html_tags, HTMLEntitiesToUnicode



def sanitize(value):

    if value is None:
        return u""

    value = remove_html_tags(value)
    value = HTMLEntitiesToUnicode(value)
    value = truncate(value)

    return value
