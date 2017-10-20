import sys
import os
import filecmp
import importlib
import datetime
import common

path = os.path.abspath('.')
sys.path.append(path)

domain = 'kouvolansanomat'
url = 'https://kouvolansanomat.fi/uutiset/lahella/edcf6384-69ec-4d8c-92c5-687e4c1c92f7'

out = 'test/parser_out.txt'
module = importlib.import_module( 'sites.' + domain )
d = module.parse(url)

class TestParser:

    @classmethod
    def setup_class(cls):
        common.initialise_file( out, d )

    def test_file_exists(self):
        common.file_exists(out)

    def test_file_not_empty(self):
        common.file_not_empty(out)

    def test_file_contents_match(self):
        common.file_contents_match(domain, out)

    def test_dictionary_created(self):
        common.dictionary_created(d)

    def test_dictionary_contains_right_keys(self):
        common.dictionary_contains_right_keys(d)

    def test_dictionary_values_correct_type(self):
        common.dictionary_values_correct_type(d)
