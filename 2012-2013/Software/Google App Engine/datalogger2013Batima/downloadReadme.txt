Instructions to export data from the application's datastore:

Ensure that the GAE sdk is already installed on your computer before 
performing these instructions

1. Update the app by stepping just outside the application folder's directory and doings:
   appcfg.py update <app-directory>

2. Generate the configuration file of the bulkloader tool
 appcfg.py create_bulkloader_config --filename=bulkloader.yaml --url=http://davidfirstapp.appspot.com/_ah/remote_api

3. Edit the file 'bulkloader.yaml' by setting connector options to the specify the format of the output file (ie csv) and 
describing how data should be transformed when exported

4. Re-run the bulkloader tool again this time by passing the configuration file as input:
 appcfg.py download_data --config_file=bulkloader.yaml --filename=readingsBatima.csv --kind=dataObject --url=http://davidfirstapp.appspot.com/_ah/remote_api
 appcfg.py download_data --config_file=bulkloader.yaml --filename=logBatima.csv --kind=FileObject --url=http://davidfirstapp.appspot.com/_ah/remote_api
