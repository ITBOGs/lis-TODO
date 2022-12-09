import psycopg2


class SqlQuery:
	def __init__(self):
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

				self.connection.autocommit = True
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

	def table_exists(self, table_name: str):
		with self.connection.cursor() as cursor:
			cursor.execute(
				f'''
				SELECT EXISTS(
				    SELECT * 
			        FROM information_schema.tables 
			        WHERE 
                        table_name = '{table_name}'
				);
				'''
			)
			return cursor.fetchone()[0]

	def create_table(self) -> None:
		with self.connection.cursor() as cursor:
			cursor.execute(
				'''
				CREATE TABLE IF NOT EXISTS category(
					category_id INT NOT NULL PRIMARY KEY,
					name VARCHAR(255) NOT NULL
				);
				
				CREATE TABLE IF NOT EXISTS task(
					task_id INT NOT NULL PRIMARY KEY,
					name VARCHAR(255) NOT NULL,
					description VARCHAR(255) NOT NULL,
					active BOOLEAN NOT NULL,
					category_id INT NOT NULL REFERENCES category (category_id)
				);
				'''
			)
