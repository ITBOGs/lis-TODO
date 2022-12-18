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

	def create_table(self) -> None:
		with self.connection.cursor() as cursor:
			cursor.execute(
				'''
				CREATE TABLE IF NOT EXISTS category(
					category_name VARCHAR(255) NOT NULL PRIMARY KEY
				);
				
				CREATE TABLE IF NOT EXISTS task(
					task_id SERIAL NOT NULL PRIMARY KEY,
					task_name VARCHAR(255) NOT NULL,
					description VARCHAR(255) NOT NULL,
					complete BOOLEAN NOT NULL DEFAULT FALSE,
					category_name VARCHAR(255) NOT NULL REFERENCES category (category_name)
				);
				'''
			)

	def get_category(self) -> tuple:
		with self.connection.cursor() as cursor:
			cursor.execute(
				'''
				SELECT category_name FROM category
				'''
			)

			return cursor.fetchall()

	def get_task(self, category_name: str) -> tuple:
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				SELECT task_name, complete FROM task
				WHERE category_name = '{category_name}'
				"""
			)

			return cursor.fetchall()

	def get_task_details(self, category_name: str, task_name: str) -> tuple:
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				SELECT task_name, description, complete FROM task
				WHERE 
					category_name = '{category_name}'
					AND task_name = '{task_name}'
					
				"""
			)

			return cursor.fetchall()

	def insert_category(self, category_name: str) -> None:
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				INSERT INTO category (category_name)
				VALUES ('{category_name}')
				"""
			)

	def insert_task(self, task_name: str, description: str, category_name: str) -> None:
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				INSERT INTO task (task_name, description, category_name)
				VALUES ('{task_name}', '{description}','{category_name}');
				"""
			)

	def del_task(self, category_name: str, task_name: str):
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				DELETE FROM task
				WHERE 
					category_name = '{category_name}'
					AND task_name = '{task_name}'
				"""
			)

	def update_task(self, task_name_new: str, description: str, category_name: str, task_name_old: str) -> None:
		with self.connection.cursor() as cursor:
			cursor.execute(
				f"""
				UPDATE task
				SET task_name = '{task_name_new}', description = '{description}'
				WHERE 
					category_name = '{category_name}'
					AND task_name = '{task_name_old}'
				"""
			)
