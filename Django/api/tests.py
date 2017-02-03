from django.test import TestCase
import os
# Create your tests here.
import sys

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(file_path+'/../SearchEngine')
sys.path.append(file_path+'/../')
import search

