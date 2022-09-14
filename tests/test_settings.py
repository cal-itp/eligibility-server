import pytest

from eligibility_server import settings
from eligibility_server.settings import Configuration


@pytest.fixture
def configuration():
    return Configuration()


@pytest.mark.usefixtures("flask")
def test_configuration_app_name(mocker, configuration: Configuration):
    assert configuration.app_name == settings.APP_NAME

    mocked_config = {"APP_NAME": "new name!"}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.app_name == "new name!"


@pytest.mark.usefixtures("flask")
def test_configuration_debug_mode(mocker, configuration: Configuration):
    assert configuration.debug_mode == settings.DEBUG_MODE

    mocked_config = {"DEBUG_MODE": False}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert not configuration.debug_mode


@pytest.mark.usefixtures("flask")
def test_configuration_host(mocker, configuration: Configuration):
    assert configuration.host == settings.HOST

    new_value = "http://example.com"
    mocked_config = {"HOST": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.host == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_log_level(mocker, configuration: Configuration):
    assert configuration.log_level == settings.LOG_LEVEL

    new_value = "ERROR"
    mocked_config = {"LOG_LEVEL": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.log_level == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_auth_header(mocker, configuration: Configuration):
    assert configuration.auth_header == settings.AUTH_HEADER

    new_value = "Some-New-Header"
    mocked_config = {"AUTH_HEADER": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.auth_header == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_auth_token(mocker, configuration: Configuration):
    assert configuration.auth_token == settings.AUTH_TOKEN

    new_value = "some-new-token"
    mocked_config = {"AUTH_TOKEN": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.auth_token == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_token_header(mocker, configuration: Configuration):
    assert configuration.token_header == settings.TOKEN_HEADER

    new_value = "Token"
    mocked_config = {"TOKEN_HEADER": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.token_header == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_client_key_path(mocker, configuration: Configuration):
    assert configuration.client_key_path == settings.CLIENT_KEY_PATH

    new_value = "./new/path"
    mocked_config = {"CLIENT_KEY_PATH": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.client_key_path == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_jwe_cek_enc(mocker, configuration: Configuration):
    assert configuration.jwe_cek_enc == settings.JWE_CEK_ENC

    new_value = "encoding"
    mocked_config = {"JWE_CEK_ENC": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.jwe_cek_enc == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_jwe_encryption_alg(mocker, configuration: Configuration):
    assert configuration.jwe_encryption_alg == settings.JWE_ENCRYPTION_ALG

    new_value = "alg"
    mocked_config = {"JWE_ENCRYPTION_ALG": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.jwe_encryption_alg == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_jws_signing_alg(mocker, configuration: Configuration):
    assert configuration.jws_signing_alg == settings.JWS_SIGNING_ALG

    new_value = "alg"
    mocked_config = {"JWS_SIGNING_ALG": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.jws_signing_alg == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_server_private_key_path(mocker, configuration: Configuration):
    assert configuration.server_private_key_path == settings.SERVER_PRIVATE_KEY_PATH

    new_path = "./new/path"
    mocked_config = {"SERVER_PRIVATE_KEY_PATH": new_path}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.server_private_key_path == new_path


@pytest.mark.usefixtures("flask")
def test_configuration_server_public_key_path(mocker, configuration: Configuration):
    assert configuration.server_public_key_path == settings.SERVER_PUBLIC_KEY_PATH

    new_path = "./new/path"
    mocked_config = {"SERVER_PUBLIC_KEY_PATH": new_path}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.server_public_key_path == new_path


@pytest.mark.usefixtures("flask")
def test_configuration_sub_format_regex(mocker, configuration: Configuration):
    assert configuration.sub_format_regex == settings.SUB_FORMAT_REGEX

    new_value = r"[a-z]\d{6}"
    mocked_config = {"SUB_FORMAT_REGEX": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.sub_format_regex == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_import_file_path(mocker, configuration: Configuration):
    assert configuration.import_file_path == settings.IMPORT_FILE_PATH

    new_value = "./new/path.csv"
    mocked_config = {"IMPORT_FILE_PATH": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.import_file_path == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_input_hash_algo(mocker, configuration: Configuration):
    assert configuration.input_hash_algo == settings.INPUT_HASH_ALGO

    new_value = "hash"
    mocked_config = {"INPUT_HASH_ALGO": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.input_hash_algo == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_csv_delimiter(mocker, configuration: Configuration):
    assert configuration.csv_delimiter == settings.CSV_DELIMITER

    new_value = "-"
    mocked_config = {"CSV_DELIMITER": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.csv_delimiter == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_csv_quoting(mocker, configuration: Configuration):
    assert configuration.csv_quoting == settings.CSV_QUOTING

    new_value = 0
    mocked_config = {"CSV_QUOTING": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.csv_quoting == new_value


@pytest.mark.usefixtures("flask")
def test_configuration_csv_quotechar(mocker, configuration: Configuration):
    assert configuration.csv_quotechar == settings.CSV_QUOTECHAR

    new_value = "$"
    mocked_config = {"CSV_QUOTECHAR": new_value}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    assert configuration.csv_quotechar == new_value
