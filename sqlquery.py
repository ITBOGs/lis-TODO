import psycopg2


class SqlQuery:
	def __init__(self):
		super(SqlQuery, self).__init__()

		self.connection = None
		self.host = '127.0.0.1'
		self.user = 'postgres'
		self.password = '2210'
		self.db_name = 'lis_todo'

	def db_connect(self) -> bool:
		for i in range(3):
			try:
				self.connection = psycopg2.connect(
					host=self.host,
					user=self.user,
					password=self.password,
					database=self.db_name
				)
				print('[INFO] Successful database connection')
				return True

			except Exception as _ex:
				print('[INFO] Error while working with postgres (connection)', _ex)

		return False

	def db_disconnect(self):
		try:
			self.connection.close()
			print('[INFO] Database disconnected')

		except Exception as _ex:
			print('[INFO] Error while working with postgres (disconnection)', _ex)
