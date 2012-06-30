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

 
