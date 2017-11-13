import sys
import os
#sys.path.insert(0, '/src/index.py')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pytest
#from src.index import *
import src.index 

def test_get_filename():
	filename = src.index.get_filename()
	assert filename != null
