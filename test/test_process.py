from system import process

pids = process.ps()

for pid in pids:
	print (pid['PID'])

