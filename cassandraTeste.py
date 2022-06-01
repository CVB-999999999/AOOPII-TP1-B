from cassandra.cluster import Cluster

cluster = Cluster(['localhost'])
session = cluster.connect('aoop')

rows = session.execute('SELECT * FROM users')
for user_row in rows:
    print(user_row.name, user_row.age, user_row.username)
