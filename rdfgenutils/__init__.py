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

