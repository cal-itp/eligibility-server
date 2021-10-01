def test_healthcheck(app, client):
  response = client.get('/healthcheck')
  assert response.status_code == 200
  assert response.data == b"Healthy"

def test_unauthorized_verify(app, client):
  response = client.get('verify')
  assert response.status_code == 403

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
  response = database.check_merchant('abc')
  assert response == True

def test_database_check_merchant_not_in_database(database):
  response = database.check_merchant('123')
  assert response == False

def test_database_check_user_in_database(database):
  response = database.check_user('A1234567', 'Garcia', ['type1'])
  assert response == ['type1']

def test_database_check_user_in_database_not_eligible(database):
  response = database.check_user('A1234567', 'Garcia', ['type2'])
  assert response == []

def test_database_check_user_not_in_database(database):
  response = database.check_user('G7778889', 'Thomas', ['type1'])
  assert response == []
