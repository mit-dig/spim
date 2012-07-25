#######################################
#######################################

Spim Project Folder
By: Yotam Aron

Below is a short description of what each file in this folder is.

- endpoint_ranges_gen.py : To generate ranges for each predicate. Not currently in use.

- endpoint_ranges.n3: Output of above file.

- errorlog: Symbolic link to the server error log.

- lib: Folder contains bulk of the code. See its readme file for more info

- reset-4store: Shell script that resets and restarts 4store endpoints at ports 81-86. These include those of the
	sparql federation project. Also resets user database for spim project (port 81)

- service_desc_gen.py: Another version endpoint_ranges_gen.py

- sparql_translate_state.txt: Used by the translation module sparql1_1.py to identify unique queries.

- spim_demo.cgi: Old version of the online demo of spim demo. Now use spim_django instead. 

- spim_django: Contains online demo for spim.py. See readme in spim_django file.

- spim_django_webID: Not in use currently, but provides webID capabilities for django.

########################################
## Setting up SPIM #####################
########################################

- First, install 4store

- Install HTTP4Store, which is the python module used to interface with 4store. Alternatively, you can adjust 
the "endpoint.py" interface to change the method with which spim interacts with the rdf storage. This is 
necessary if 4store is not used, though it will be more complicated to do so.

- Set up the 4store databases. The following is where the 4store databases are currently set up

		*sparqlfed_article: contains article_categories_en.nt.bz2, at port 82
		*sparqlfed_category: contains category_labels_en.nt.bz2, at port 83
		*sparqlfed_persondata: contains persondata_en.nt.bz2, at port 84
		*sparqlfed_mappingbased_infoboxes: contains yago_links.nt at port 85
		*userProfiles: Contains profiles for users for differential privacy purposes at port 86
		*internetData: Contains census data for towns at port 81

The first four are part of the sparql federation project and were obtained from dbpaedia. 
For more information on what data is stored there, consult the project folder. 
"userProfiles" holds the epsilon values for users in the spim module. 
"internetData" is the current data used to test the module (subject to change)	

- If for any reason you changed the port locations where the 4stores were running, or if you need to set
spim up on a different server or directory, you will need to set up the paths in all the files. These are
usually located at the top of the files. The two most important files are the spim file, in "lib/spim.py"; 
the translation module, located in "lib/sparql1_1n3.py", and the spim_module app in the django server, 
located in "spim_django/spim_module/views.py."


########################################
## RUNNING SPIM ########################
########################################

- Running Django

	To run django, go into the spim_django folder. The command is:

	sudo python manage.py runserver 0:[port number]

	where [portnumber] is replaced with the port number. This will start the django server in the port number specified. For more information on django servers, look at the django version 1.4 documentation online. Currently, the wsgi is not enabled so the server cannot run at the same port as apache.

- Resetting 4store

	To reset the 4store servers, and delete the user profiles for the spim module, run the reset 4store 
	bash file:

	sudo ./reset-4store

	You should edit this bash file if you change the default port numbers. In addition, this command resets 
	the  
