from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='vitoria')

image = cloud.create_image(
    'ubuntu-trusty', filename='ubuntu-trusty.qcow2', wait=True)

flavor = cloud.get_flavor_by_ram(512)

instance_name = 'testing'

def create_instance(instance_name):
	testing_instance = conn.create_server(wait=True, auto_ip=True,
    	name=instance_name,
    	image=image,
    	flavor=flavor,
    	keypair=keypair_name,
    	security_groups=[sec_group_name],
    	userdata=ex_userdata)

	f_ip = conn.available_floating_ip()
	print('The Fractals app will be deployed to http://%s' % f_ip['floating_ip_address'] )

def delete_instance(instance_name):
	conn.delete_server(name_or_id=instance_name)

keypair = generate_keypair('demokey')
pub_key_file = '/home/username/.ssh/id_rsa.pub'

def generate_keypair(keypair_name):
	if conn.search_keypairs(keypair_name):
		print("Keypair already exists. Skipping import.")
	else:
		print('Adding keypair...')
		conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())
	for keypair in conn.list_keypairs():
		print(keypair)

sec_group_name = create_security_group('all-in-one')

def create_security_group(sec_group_name):
	if conn.search_security_groups(sec_group_name):
		print("Security group already exists. Skipping creation.")
	else:
	    print('Creating security group.')
	    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
	    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
	    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

	conn.search_security_groups(sec_group_name)

ex_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''



