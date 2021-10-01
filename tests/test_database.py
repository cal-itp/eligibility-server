"""
Test database class and methods
"""
import json

with open("data/server.json") as f:
  DATA = json.load(f)

def test_database_init(database):
  assert database._config
  assert database._merchants
  assert database._users

def test_database_properties(database):
  assert database.auth_header
  assert database.auth_token
  assert database.token_header
  assert database.jwe_cek_enc
  assert database.jwe_encryption_alg
  assert database.jws_signing_alg
  assert database.request_access

def test_database_check_merchant_in_database(database):
  merchant_id = DATA['merchants'][1]
  response = database.check_merchant(merchant_id)
  assert response == True

def test_database_check_merchant_not_in_database(database):
  merchant_id_not_in_database = '123'
  response = database.check_merchant(merchant_id_not_in_database)
  assert response == False

def test_database_check_user_in_database(database):
  key = min(DATA['users'])
  user = DATA['users'][key][0]
  types = DATA['users'][key][1]
  response = database.check_user(key, user, types)
  assert response == types

def test_database_check_user_in_database_not_eligible(database):
  key = min(DATA['users'])
  user = DATA['users'][key][0]
  types = ['type2']
  response = database.check_user(key, user, types)
  assert response == []

def test_database_check_user_not_in_database(database):
  response = database.check_user('G7778889', 'Thomas', ['type1'])
  assert response == []

