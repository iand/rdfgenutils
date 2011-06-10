# Text utilities
import re
import htmlentitydefs

url_re = re.compile(
    r'^https?://' # http:// or https://
    r'(?:(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|/\S+)$', re.IGNORECASE)

def slugify(str):
  removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
  aslug = strip_markup(str)
  for a in removelist:
      aslug = re.sub(r'\b'+a+r'\b','',aslug)
  aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
  aslug = re.sub('-', ' ', aslug)
  aslug = re.sub('\s+', '-', aslug)
  return aslug

def propertify(str):
  removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
  aslug = strip_markup(str)
  for a in removelist:
      aslug = re.sub(r'\b'+a+r'\b','',aslug)
  aslug = re.sub('[^\w]', '', aslug.title()).strip()
  if len(aslug) > 1:
    return aslug[0].lower()+aslug[1:]
  else:
    return aslug

def strip_ws(text):
  """Strips whitespace from the input text"""
  text = re.sub('\s+', '', text, re.S)
  return text

def strip_markup(data):

  data = re.sub(r'&(#?)(.+?);',convertentity,data)
  data = re.sub('<[^>]+>', '', data)
  data = re.sub('&amp;', '&', data)
  data = re.sub('&lt;', '<', data)
  data = re.sub('&gt;', '>', data)
  data = re.sub('&quot;', '"', data)
  data = re.sub('&[a-z]+;', ' ', data)
  data = re.sub('\s\s+', ' ', data)
  data = data.strip()
  return data


def convertentity(m):
  if m.group(1)=='#':
    try:
      return chr(int(m.group(2)))
    except ValueError:
      return '&#%s;' % m.group(2)
  try:
    return htmlentitydefs.entitydefs[m.group(2)]
  except KeyError:
    return '&%s;' % m.group(2)


def clean_uri(data):
  """Cleans up common invalid characters in URIs"""
  data = data.replace(' ', '%20').replace('"', '%22').replace('<', '%3C').replace('>', '%3E').replace('{', '%7B').replace('}', '%7D') 
  data = data.replace('|', '%7C').replace('\\', '%5C').replace('^', '%5E').replace('~', '%7E').replace('[', '%5B').replace(']', '%5D') 
  data = data.replace('&amp;', '&')
  return data

def is_uri(data):
  if url_re.search(data):
    return True
  else:
    return False

def literal(data):
  return re.sub(r'"', r'\\"', ntencode(data))

def ntencode(unicode_data, encoding="ascii"):
  #return unicode_data.encode(encoding,'ignore') # TODO: remove shortcut
  
  """Emulate Python 2.3's 'xmlcharrefreplace' encoding error handler."""
  chars = []

  # nothing to do about xmlchars, but replace newlines with escapes: 
  unicode_data=unicode_data.replace("\n","\\n")

  try:
    encoded = unicode_data.encode(encoding, 'strict')
    return encoded
  except UnicodeError:

    # Step through the unicode_data string one character at a time in
    # order to catch unencodable characters:
    for char in unicode_data:
        try:
            chars.append(char.encode(encoding, 'strict'))
        except UnicodeError:
            chars.append('\u%04X' % ord(char))
    return ''.join(chars)
    
def triple(s, p, o, lang_or_dt=''):
  ret = ''
  if s.startswith('http'):
    ret += '<%s>' % s
  else:
    ret += s
  
  ret += ' '
  if p =='a':
    ret += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
  elif p.startswith('rdf:'):
    ret += '<http://www.w3.org/1999/02/22-rdf-syntax-ns#%s>' % p[4:]
  elif p.startswith('rdfs:'):
    ret += '<http://www.w3.org/2000/01/rdf-schema#%s>' % p[5:]
  elif p.startswith('owl:'):
    ret += '<http://www.w3.org/2002/07/owl#%s>' % p[4:]
  elif p.startswith('dc:'):
    ret += '<http://purl.org/dc/terms/%s>' % p[3:]
  elif p.startswith('ov:'):
    ret += '<http://open.vocab.org/terms/%s>' % p[3:]
  elif p.startswith('foaf:'):
    ret += '<http://xmlns.com/foaf/0.1/%s>' % p[5:]
  elif p.startswith('geo:'):
    ret += '<http://www.w3.org/2003/01/geo/wgs84_pos#%s>' % p[4:]
  elif p.startswith('skos:'):
    ret += '<http://www.w3.org/2004/02/skos/core#%s>' % p[5:]
  else:
    ret += '<%s>' % p
  
  ret += ' '
  if o.startswith('http'):
    ret += '<%s>' % o
  elif o.startswith('_:'):
    ret += '%s' % o
  else:
    ret += '"%s"' % o.replace('"', r'\"')
    
    if lang_or_dt:
      if lang_or_dt.startswith('xsd:'):
        ret += '^^<http://www.w3.org/2001/XMLSchema#%s>' % lang_or_dt[4:]
      elif lang_or_dt.isalpha():
        ret += '@%s' % lang_or_dt
    
  ret += " .\n"
  return ret    
