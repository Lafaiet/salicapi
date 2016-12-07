from htmllaundry import strip_markup
from BeautifulSoup import BeautifulStoneSoup
import cgi



def validate_cpf( cpf ):
    """ 
    Method to validate a brazilian CPF number 
    Based on Pedro Werneck source avaiable at
    www.PythonBrasil.com.br
    
    Tests:
    >>> print Cpf().validate('91289037736')
    True
    >>> print Cpf().validate('91289037731')
    False
    """
    cpf_invalidos = [11*str(i) for i in range(10)]
    if cpf in cpf_invalidos:
        return False
   
    if not cpf.isdigit():
        """ Verifica se o CPF contem pontos e hifens """
        cpf = cpf.replace( ".", "" )
        cpf = cpf.replace( "-", "" )

    if len( cpf ) < 11:
        """ Verifica se o CPF tem 11 digitos """
        return False
        
    if len( cpf ) > 11:
        """ CPF tem que ter 11 digitos """
        return False
        
    selfcpf = [int( x ) for x in cpf]
    
    cpf = selfcpf[:9]
    
    while len( cpf ) < 11:
    
        r =  sum( [( len( cpf )+1-i )*v for i, v in [( x, cpf[x] ) for x in range( len( cpf ) )]] ) % 11
    
        if r > 1:
            f = 11 - r
        else:
            f = 0
        cpf.append( f )
    
    
    return bool( cpf == selfcpf )



def truncate(word, truncate_size=200):
    if word is None:
        return ""
        
    return  word[:truncate_size]

def remove_blanks(word):
    if word is None:
        return ""

    return word.split()[0]

def cgccpf_mask(cgccpf):

    if validate_cpf(cgccpf):
        cgccpf = '******'+cgccpf[6:]

    return cgccpf

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
