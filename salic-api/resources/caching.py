from flask import request

def make_key ():
  """Make a key that includes GET parameters."""
  return request.full_path
