import datetime
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from src.core.data_source import engine
from src.models.M_SETTINGS import M_SETTINGS
from src.models.M_SETTINGS_DATE import M_SETTINGS_DATE
from src.models.M_REQUEST_PARAMETERS import M_REQUEST_PARAMETERS


# Дочерний класс SettingsCreator формирует структуру настроек при инициализации объекта и
# возвращает полученную структуру, либо её JSON сериализацию
class SettingsCreator(ABC):
    _m_settings: Dict[str, Any]
    _m_request_parameters: Dict[str, Any]
    _m_settings_date: Dict[str, Any]

    _settings: Dict[str, Any]
    _requested_settings_list: List[str]
    _used_tables: List[str]

    def __init__(self, requested_settings_list):
        self._requested_settings_list = requested_settings_list
        self._used_tables = list()
        self._settings = dict()
        try:
            self._prepare_m_settings_date()
            self._prepare_m_settings()
            self._prepare_m_request_parameters()
        except Exception as e:
            logging.error("Не удалось получить настройки КСУП кэшера из БД: %s", str(e))
            raise

        self._create()

    def _create(self):
        for requested_setting in self._requested_settings_list:
            if requested_setting in ["LIST_CHANNEL_CODES", "LIST_CUSTOMER_PROFILES", "LIST_PRODUCT_TYPES"]:
                # парсинг CSV значений
                self._used_tables.append("M_SETTINGS")
                self._settings[requested_setting] = list(self._m_settings[requested_setting].split(","))
            elif requested_setting == "TIMEOUT":
                # в БД в миллисекундах, а в приложении в секундах
                self._used_tables.append("M_SETTINGS")
                self._settings[requested_setting] = int(self._m_settings[requested_setting]) // 1000
            elif requested_setting in ["REPEAT_COUNT", "REPEAT_INTERVAL", "LOGGING_LEVEL"]:
                # числа
                self._used_tables.append("M_SETTINGS")
                self._settings[requested_setting] = int(self._m_settings[requested_setting])
            elif requested_setting == "REQUEST_PARAMETERS":
                # словарь настроек из REQUEST_PARAMETERS
                self._used_tables.append("REQUEST_PARAMETERS")
                self._settings["REQUEST_PARAMETERS"] = dict()
                for request_parameters_row in self._m_request_parameters:
                    if request_parameters_row["product_type"] not in self._settings["REQUEST_PARAMETERS"]:
                        self._settings["REQUEST_PARAMETERS"][request_parameters_row["product_type"]] = dict()
                    self._settings["REQUEST_PARAMETERS"][request_parameters_row["product_type"]][
                        request_parameters_row["parameter_code"]] = request_parameters_row["column_name"]
            else:
                if requested_setting in self._m_settings:
                    self._used_tables.append("M_SETTINGS")
                    self._settings[requested_setting] = self._m_settings[requested_setting]
                else:
                    logging.error("Не удалось найти параметр %s в таблице M_SETTINGS, либо не задан алгоритм его "
                                  "формирования",
                                  requested_setting)
                    raise ValueError("Запрошен неизвестный параметр настроек " + requested_setting)

    def get_time_last_maintained(self) -> datetime.datetime:
        files_maintained_dates = list()
        for table_name, maintained_date in self._m_settings_date.items():
            if table_name in self._used_tables:
                files_maintained_dates.append(maintained_date)
        return max(files_maintained_dates)

    def get_json(self) -> str:
        return json.dumps(self._settings)

    def get_settings(self) -> str:
        return self._settings

    def _prepare_m_settings(self):
        logging.info("Получение настроек M_SETTINGS из БД")
        try:
            with engine.connect() as connection:
                self._m_settings = dict(connection.execute(
                    M_SETTINGS.select().with_only_columns(M_SETTINGS.c.key, M_SETTINGS.c.value)).fetchall())
        except Exception as e:
            logging.error("При получении настроек M_SETTINGS произошла ошибка: %s", str(e))
            raise

    def _prepare_m_request_parameters(self):
        logging.info("Получение настроек M_REQUEST_PARAMETERS из БД")
        try:
            with engine.connect() as connection:
                self._m_request_parameters = list(connection.execute(
                    M_REQUEST_PARAMETERS.select().with_only_columns(M_REQUEST_PARAMETERS.c.product_type,
                                                                    M_REQUEST_PARAMETERS.c.column_name,
                                                                    M_REQUEST_PARAMETERS.c.parameter_code)).fetchall())
        except Exception as e:
            logging.error("При получении настроек M_REQUEST_PARAMETERS произошла ошибка: %s", str(e))
            raise

    def _prepare_m_settings_date(self):
        logging.info("Получение настроек M_SETTINGS_DATE из БД")
        try:
            with engine.connect() as connection:
                self._m_settings_date = dict(connection.execute(
                    M_SETTINGS_DATE.select().with_only_columns(M_SETTINGS_DATE.c.table_name,
                                                               M_SETTINGS_DATE.c.sdate)).fetchall())
        except Exception as e:
            logging.error("При получении настроек M_SETTINGS_DATE произошла ошибка: %s", str(e))
            raise
