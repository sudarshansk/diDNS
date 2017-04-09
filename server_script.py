import dns_server as dns

servers = [1200,1300]
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})

serv_num = input('\nEnter number of servers to run\n')

servers = servers[:serv_num]


	