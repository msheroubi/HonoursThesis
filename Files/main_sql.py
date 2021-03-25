import os
import csv
import pyodbc
import time
import random

current_milli_time = lambda: int(round(time.time() * 1000))

def reset(cursor):
	with open('proxi_mk01.ddl','r') as f:
		sqlScript = f.read()
		statements = sqlScript.split(';')
		start_time = current_milli_time()
		for statement in statements:
			statement += ';'
			cursor.execute(statement)
			cursor.commit()

def runSQL(size):
	print('Running SQL')
	results = {'ID': 'SQL', 'SIZE': size}

	# SQL SERVER
	sqlexpress02 = 'Server=localhost\\SQLEXPRESS02;Database=master;Trusted_Connection=True;'
	# print("Establishing Connection...")

	start_time = current_milli_time()
	sql_conn = pyodbc.connect('Driver={SQL Server};'
	                      'Server=localhost\\SQLEXPRESS02;'
	                      'Database=master;'
	                      'Trusted_Connection=yes;')
	end_time = current_milli_time()

	run_time = end_time - start_time
	# print("Connected in {} ms".format(run_time))
	results['EC'] = run_time
	cursor = sql_conn.cursor()

	err_line = ''
	try:
		# Define Model
		# print("Defining Model...")
		inputdir = 'proxi_mk01.ddl'

		# with open(inputdir,'r') as f:
		# 	sqlScript = f.read()
		# 	statements = sqlScript.split(';')
		# start_time = current_milli_time()
		# reset(cursor)
		# # 	for statement in statements:
		# # 		statement += ';'
		# # 		cursor.execute(statement)
		# end_time = current_milli_time()
		# run_time = end_time - start_time
		# # print("Model Defined in {} ms".format(run_time))
		# results['DD'] = [run_time]

		# # num_runs = [1, 5, 10, 100, 250, 500]
		# # for run in num_runs:
		# # 	print("Loading {} of data...".format(run))
		# # 	with open('sql_data.sql', 'r') as f:
		# # 		start_time = current_milli_time()
		# # 		for i in range(0, run):
		# # 			line = next(f)
		# # 			err_line = line
		# # 			cursor.execute(line)
		# # 			cursor.commit()
		# # 		end_time = current_milli_time()
		# # 		run_time = end_time - start_time
		# # 		print("Data loaded in {} ms".format(run_time))
		# # 		results['DL{}'.format(run)] = run_time

		# # Resetting
		# # print("Resetting...")
		# with open(inputdir,'r') as f:
		# 	sqlScript = f.read()
		# 	statements = sqlScript.split(';')
		# 	start_time = current_milli_time()
		# 	for statement in statements:
		# 		statement += ';'
		# 		cursor.execute(statement)
		# 	end_time = current_milli_time()
		# 	run_time = end_time - start_time
		# # print("Model Defined in {} ms".format(run_time))
		# results['DD'].append(run_time)


		# # Load All Data
		# # print("Loading All Data...")
		# with open('sql_data.sql', 'r') as f:
		# 	start_time = current_milli_time()
		# 	for line in f:
		# 		err_line = line
		# 		try:
		# 			cursor.execute(line)
		# 			cursor.commit()
		# 		except:
		# 			print("FAILED: " + err_line)
		# 	end_time = current_milli_time()
		# 	run_time = end_time - start_time
		# 	# print("Data loaded in {} ms".format(run_time))
		# 	results['DL*'] = run_time

		# Run Queries
		queries = []
		queries.append("SELECT * FROM Users WHERE user_id = {};")
		# queries.append("SELECT * FROM Users WHERE user_name = 'craigjohn';")
		queries.append("SELECT Y.name FROM Users AS X, Users as Y, User_to_Interest as UI  WHERE X.user_id = {} AND X.user_id = UI.user_id AND Y.user_id IN (SELECT SUI.user_id FROM User_to_Interest as SUI WHERE SUI.interest_id = UI.interest_id AND NOT SUI.user_id = X.user_id);")
		queries.append("SELECT U.user_name FROM Users as U, isFriendsWith as IFW WHERE IFW.user_id = {} AND IFW.friend_id = U.user_id")
		queries.append("SELECT DISTINCT G.group_name FROM Users as U, Groups as G, isFriendsWith as IFW, isMember as IM WHERE U.user_id = {} AND G.group_id = IM.group_id AND U.user_id = IFW.user_id AND IFW.friend_id = IM.user_id;")
		queries.append("SELECT U.user_name FROM Users as U, Events as E, isMember as IM, isAttending as IA WHERE IM.user_id = {} AND E.group_id = IM.group_id AND IA.event_id = E.event_id AND IA.user_id = U.user_id;")
		queries.append("SELECT I.interest_name FROM User_to_Interest as UI, Group_to_Interest as GI, Events as E, isAttending as IA, User_to_Interest as UI2, Interests as I WHERE UI.user_id = {} AND UI.interest_id = GI.interest_id AND E.group_id = GI.group_id AND IA.event_id = E.event_id AND IA.user_id = UI2.user_id AND UI2.interest_id = I.interest_id;")


		query_tags = []
		num_runs = 1
		num_repeats = 100
		for j in range(0, num_runs):
			for i in range(0, len(queries)):
				# print("Running Query ", i)
				start_time = current_milli_time()
				for x in range(0, num_repeats):
					user_id = random.randint(1, 1000)
					rst = cursor.execute(queries[i].format(user_id))
					count = 0
					for ele in rst:
						count += 1
				end_time = current_milli_time()
				run_time = end_time - start_time
				# print("Query {} ran in {} ms".format(i, run_time))
				tag = 'Q{} - {}'.format(i, num_repeats)
				results[tag] = run_time
				query_tags.append(tag)

		for tag in query_tags:
			results[tag] = results[tag] / num_runs

		with open("sql-results.csv", "a", newline='') as f:
			writer = csv.writer(f)
			for key, value in results.items():
				writer.writerow([key, value])
			f.write('||')
	except Exception as e:
		print(err_line)
		print(e)
	finally:
		print(results)
		sql_conn.close()

# cursor.execute('SELECT * FROM Users')
# for row in cursor:
#     print(row)

# print("Dropping Tables...")
# with open('sql_drop_tables.sql', 'r') as f:
# 	start_time = current_milli_time()
# 	for line in f:
# 		err_line = line
# 		cursor.execute(line)
# 		cursor.commit()
# 	end_time = current_milli_time()
# 	run_time = end_time - start_time
# 	print("Tables Dropped in {} ms".format(run_time))
# 	results['DT'] = run_time

runSQL(100000)