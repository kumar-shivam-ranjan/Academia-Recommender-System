import psycopg2
import subprocess
conn = psycopg2.connect("dbname=explo user=explo password=explo")
file=r"/home/parzival3219/recommender/Barc-modified/run.sh"
table="recommender_barcrequest"
cur=conn.cursor()
i=0

cur.execute(f'SELECT * FROM {table} WHERE result_generated IS FALSE;');
rows = cur.fetchall()
for row in rows:
    # print(row)
    # print(row[0])
    token=row[1]

    # print(token)
    # subprocess.run(["py","-3",file,token])
    # subprocess.Popen(["bash", file, token])
    # cur.execute("UPDATE REQUESTS SET DONE=TRUE WHERE TITLE=%s",(row[0],))
    conn.commit()
		i+=1     
