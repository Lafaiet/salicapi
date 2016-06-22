from htmllaundry import strip_markup
from BeautifulSoup import BeautifulStoneSoup
import cgi


def truncate(word, truncate_size=200):
    if word is None:
        return ""
        
    return  word[:truncate_size]

def remove_blanks(word):
    if word is None:
        return ""

    return word.split()[0]

def remove_html_tags(word):
    if word is None:
        return ""

    return strip_markup(word)


def HTMLEntitiesToUnicode(word):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    if word is None:
        return ""

    word = unicode(BeautifulStoneSoup(word, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return word

def unicodeToHTMLEntities(word):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    word = cgi.escape(word).encode('ascii', 'xmlcharrefreplace')
    return text
