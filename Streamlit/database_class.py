import mysql.connector
import numpy as np
import pandas as pd

class DB:
	def __del__(self):
		self.mydb.close()

	def __init__(self, databaseConfig):
		self.mydb = mysql.connector.connect(  
				host=databaseConfig.host,
				user=databaseConfig.user,
				password=databaseConfig.password,
				database=databaseConfig.database
		)
		print("Started database connection")
    
	#Make randon
	def get_test_list(self, num):
		cur = self.mydb.cursor()
		cur.execute("SELECT person_id, IFNULL(description,'') FROM twitter_profiles ORDER BY twitter_profiles.person_id ASC limit %d;" % num)
		myresult = cur.fetchall()

		test_list = np.array(myresult)
		test_list.reshape((len(test_list), len(test_list[0])))

		cur.close()

		return test_list

	
	def sql_executor(self, query):
		cur = self.mydb.cursor()

		cur.execute(query)
		cols = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		df = pd.DataFrame(data, columns=cols)
		
		cur.close()
		return df
	
	def query_by_id(self, id):
		cur = self.mydb.cursor()
		cur.execute("SELECT * FROM twitter_profiles WHERE id = %d;" % id)
		cols = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		df = pd.DataFrame(data, columns=cols)
		
		cur.close()
		return df
	
	def query_by_text(self, attr, text):
		cur = self.mydb.cursor()
		cur.execute("SELECT * FROM twitter_profiles WHERE %s = '%s';" % (attr, text))
		cols = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		df = pd.DataFrame(data, columns=cols)
		
		cur.close()
		return df
	

# TODO finish
"""
	def query_by_followers(self, attr, num):
		cur = self.mydb.cursor()

		
		cols = [desc[0] for desc in cur.description]
		data = cur.fetchall()
		df = pd.DataFrame(data, columns=cols)
		
		cur.close()
		return df
"""