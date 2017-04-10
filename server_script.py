import os

servers = [1200,1300]
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})

serv_num = input('\nEnter number of servers to run\n')
servers = servers[:serv_num]
a=' '
for port in servers:
	a = a + str(port) + ' '
print a
server_paths=[]
for port in servers:
	dns_path='cases/case1'
	dns_path = dns_path+'/'+str(port)+'.txt '
	print dns_path
	cmd = "python dns_server.py "+str(port)+" "+dns_path+a
	boo = "gnome-terminal -x sh -c \"xdotool getactivewindow; "+cmd+"; bash\""
	os.system(boo)


#"gnome-terminal -x sh -c \"xdotool getactivewindow windowminimize; aplay draw.wav; exit; bash\""