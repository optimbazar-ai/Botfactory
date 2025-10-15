import sqlite3

conn = sqlite3.connect('instance/botfactory.db')
cursor = conn.cursor()

# Check bots
cursor.execute("SELECT * FROM bots")
bots = cursor.fetchall()

print("BOTS IN DATABASE:", len(bots))
for bot in bots:
    print(bot)

conn.close()
