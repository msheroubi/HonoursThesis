import re

sql_file = open("sql_data.sql", "r")
cypher_node_file = open("cypher_node_data.cql", "r")
cypher_rel_file = open("cypher_rel_data.cql", "r")

sql_lines = sql_file.read().splitlines()
cypher_node_lines = cypher_node_file.read().splitlines()
cypher_rel_lines = cypher_rel_file.read().splitlines()

#Isolates data portion of the insert statements (Finds last index of '(')
def trimSQL(temp_sql_lines):
	out = []
	for line in temp_sql_lines:
		brMarker = line.rindex('(')
		lenLine = len(line)
		line = line[brMarker+1:lenLine-2]
		components = re.split(r", (?=')|,|:", line)
		out.append(components)
	return out

def trimCypherNodes(temp_cypher_nodes):
	out = []
	for line in temp_cypher_nodes:
		brMarker = line.rindex('{')
		lenLine = len(line)
		line = line[brMarker+1:lenLine-3]
		out.append(line)

	result = []
	for line in out:
		components = re.split(r", (?=')|,|:", line)
		components = components[1::2]
		result.append(components)

	return result

#Returns number of rows that fully match with cypher node
def testUserData(num_users, num_attributes, cypher_data, sql_data):
	row_passes = 0
	for i in range(0, num_users):
		col_passes = 0
		for j in range(0, num_attributes):
			print(cypher_data[i][j])
			print(sql_data[i][j])
			if cypher_data[i][j] == sql_data[i][j]:
				col_passes +=1
		if col_passes == num_attributes:
			row_passes += 1
		else:
			print("XXX")
	return row_passes

#print(trimCypherNodes(cypher_node_lines))
#print(trimSQL(sql_lines))

cypher_data = trimCypherNodes(cypher_node_lines)
sql_data = trimSQL(sql_lines)

print(testUserData(25,7, cypher_data, sql_data))

cypher_node_file.close()
cypher_rel_file.close()
sql_file.close()
