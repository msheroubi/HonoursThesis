from neo4j import GraphDatabase, basic_auth
import time
import csv
import random

current_milli_time = lambda: int(round(time.time() * 1000))
def reset(cursor):
	cursor.run("MATCH (n) DETACH DELETE n")
	cursor.sync()

def runNeo(size):
	print('Running Neo')
	results = {'ID': 'Neo4j', 'SIZE': size}
	# Neo4j

	start_time = current_milli_time()
	neo_driver = GraphDatabase.driver('<connection address>', auth=basic_auth('<user>', '<pass>'), max_connection_lifetime=0, keep_alive=True)
	neo_db = neo_driver.session()
	end_time = current_milli_time()
	run_time = end_time - start_time
	results['EC'] = run_time

	# We can skip the define model step since Neo4j doesn't need one to be defined

	err_line = ''
	try:
		# # Delete Everything
		# # print("Resetting...")
		# start_time = current_milli_time()
		# # neo_db.run("MATCH (n) DETACH DELETE n")
		reset(neo_db)
		# end_time = current_milli_time()
		# run_time = end_time - start_time
		# results['DT'] = run_time

		count = 0
		laps = 0
		# Load Node Data
		# print("Loading Node Data...")
		with open('cypher_node_data.cql', 'r') as f:
			start_time = current_milli_time()
			for line in f:
				err_line = line
				neo_db.run(line)
				if count > 1000:
					count = 0
					neo_db.sync()
					laps += 1
				count += 1
			end_time = current_milli_time()
			run_time = end_time - start_time
			# print("Node data loaded in {} ms".format(run_time))
			results['DL-N'] = run_time

		# Load Relationship Data
		# print("Load Relationship Data...")
		count = 0
		laps = 0
		with open('cypher_rel_data.cql', 'r') as f:
			start_time = current_milli_time()
			for line in f:
				err_line = line
				neo_db.run(line)
				count+=1
				if count > 4000:
					# print("Reconnecting...")
					# neo_driver = GraphDatabase.driver('<connection address>', auth=basic_auth('<user>', '<pass>'))
					# neo_db = neo_driver.session()
					neo_db.sync()
					laps += 1
					count = 0
			end_time = current_milli_time()
			run_time = end_time - start_time
			# print("Relationsihp data loaded in {} ms".format(run_time))
			print(count)
			print(laps)
			results['DL-R'] = run_time

		# Run Queries
		queries = []
		# queries.append("MATCH (u:User) WHERE u.user_name = 'craigjohn' RETURN u;")
		queries.append("MATCH (u:User) WHERE u.user_id = {} RETURN u;")
		queries.append("MATCH (x:User)-[:hasInterest]->(i:Interest)<-[:hasInterest]-(y:User) WHERE x.user_id = {} RETURN y;")
		queries.append("MATCH (x:User), (y:User) WHERE x.user_id = {} AND (x)-[:isFriendsWith]->(y) RETURN y;")
		queries.append("MATCH (x:User)-[:isFriendsWith]->(y:User)-[:isMember]->(g:Group) WHERE x.user_id = {} RETURN g;")
		queries.append("MATCH (u:User)-[r:isMember]->(g:Group)-[c:creates]->(e:Event)<-[:isAttending]-(y:User) WHERE u.user_id = {} RETURN y;")
		queries.append("MATCH (x:User)-[:hasInterest]->(i:Interest)<-[:hasInterest]-(g:Group)-[:creates]->(e:Event)<-[:isAttending]-(y:User)-[:hasInterest]->(j:Interest) WHERE x.user_id = {} RETURN j;")
		# queries.append("MATCH (n)-[]->(m) RETURN n, m")
		
		query_tags = []
		num_runs = 1
		num_repeats = 100

		for j in range(0, num_runs):
			for i in range(0, len(queries)):
				# print("Running Query ", i)
				start_time = current_milli_time()
				for x in range(0, num_repeats):
					user_id = random.randint(1, 1000)
					rst = neo_db.run(queries[i].format(user_id))
					count = 0
					for ele in rst:
						count += 1
					# print(count)
				end_time = current_milli_time()
				run_time = end_time - start_time
				# print("Query {} ran in {} ms".format(i, run_time))
				tag = 'Q{} - {}'.format(i, num_repeats)
				if tag in results:
					results[tag] += run_time
				else:
					results[tag] = run_time
					query_tags.append(tag)

		for tag in query_tags:
			results[tag] = results[tag] / num_runs

		with open("neo4j-results.csv", "a", newline='') as f:
			writer = csv.writer(f)
			for key, value in results.items():
				writer.writerow([key, value])
			f.write('||')
	except Exception as e:
		print(err_line)
		print(e)
	finally:
		neo_driver.close()
		print(results)
