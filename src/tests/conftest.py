# import pytest
# from unittest.mock import MagicMock
#
# def pytest_configure(config):
#     """
#     Настраивает мок для Settings до импорта модулей.
#     """
#     from unittest.mock import patch
#     # Патчим модуль, а не класс, чтобы избежать импорта Settings
#     patcher = patch("src.core.config.settings", new=MagicMock())
#     mock_settings = patcher.start()
#     mock_settings.DB_USER = "test_user"
#     mock_settings.DB_PASSWORD = "test_password"
#     mock_settings.DB_HOST = "localhost"
#     mock_settings.DB_NAME = "test_db"
#     mock_settings.ALGORITHM = "HS256"
#     mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
#     mock_settings.REFRESH_TOKEN_EXPIRE_DAYS = 7
#     mock_settings.SECRET_KEY = "test_secret_key"
#     config._settings_patch = patcher
#     print("Mocked settings in pytest_configure")
#
# def pytest_unconfigure(config):
#     """
#     Очищает мок после тестов.
#     """
#     if hasattr(config, "_settings_patch"):
#         config._settings_patch.stop()
