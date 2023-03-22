from types import SimpleNamespace
from sqlalchemy import create_engine
import pandas as pd
from connection_type import Types

#FIXME bring back Types Connection back
class eCairnConnector:
	def __init__(self, method: Types.Connection, **kwargs):
		self._kwargs = kwargs
		self._data = None

		if method == Types.Connection.FROM_TYPE_DB:
			if "db_config" not in self._kwargs.keys():
				raise ValueError("Expected to find value for `db_config`. No value found.")
			elif type(self._kwargs["db_config"]) != SimpleNamespace:
				raise TypeError("Expected to find type {} for `db_config`. Found type {}.".format(SimpleNamespace, type(self._kwargs["db_config"])))
			else:
				if "limit" in self._kwargs.keys():
					self._from_db(self._kwargs["db_config"], limit=self._kwargs["limit"])
				else:
					self._from_db(self._kwargs["db_config"])

		elif method == Types.Connection.FROM_TYPE_CSV:
			if "csv_filename" not in self._kwargs.keys():
				raise ValueError("Expected to find value for `csv_filename`. No value found.")
			elif type(self._kwargs["csv_filename"]) != str:
				raise TypeError("Expected to find type {} for `csv_filename`. Found type {}.".format(str, type(self._kwargs["csv_filename"])))
			else:
				self._from_csv(self._kwargs["csv_filename"])

		elif method == Types.Connection._READ_ID_LIST:
			if "limit" in self._kwargs.keys():
				self._query_db_by_id(self._kwargs["id_list"], limit = self._kwargs["limit"])
			else:
				self._query_db_by_id(self._kwargs["id_list"])


	def _from_db(self, databaseConfig:SimpleNamespace, limit=1000) -> None:
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		self._data = pd.read_sql(f"SELECT person_id, IFNULL(description,'') FROM twitter_profiles ORDER BY twitter_profiles.person_id ASC limit {limit};", engine)

	def _from_csv(self, file:str) -> None:
		self._data = pd.read_csv(file, index_col=0)

	def _query_db_by_id(self, databaseConfig:SimpleNamespace, ref_list:list, limit = 10000) -> None:
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		self._data = pd.read_sql(f"SELECT person_id, IFNULL(description,'') FROM twitter_profiles WHERE person_id IN ({','.join(map(lambda x: str(x), ref_list))}) ORDER BY twitter_profiles.person_id ASC limit {limit};", engine)

	def get_dataframe(self) -> pd.DataFrame:
		return self._data

	@classmethod
	def get_eCairn_byID(cls, db_config:SimpleNamespace, ref_list:list) -> pd.DataFrame:
		new_instance = cls(Types.Connection._READ_ID_LIST, db_config=db_config, id_list = ref_list)
		return new_instance.get_dataframe()
        