# Script for "booting" AppEngine environment. 
# Place this at ~/.ipython and then "import gae; gae.setup()" from ipython shell

# http://tech.einaregilsson.com/2010/10/11/unit-testing-model-classes-in-google-app-engine/#more-416
def setup(dbfile=None, fresh=0):
    from os.path import isfile
    import yaml
    from os import environ, remove

    appfile = "app.yaml"

    if isfile(appfile):
        doc = yaml.load(open(appfile))
        app_id = doc["application"]
    else:
        app_id = "dummyapp"

    dbfile = dbfile or "/tmp/dev_appserver.datastore"

    environ["APPLICATION_ID"] = app_id
    if fresh and isfile(dbfile):
        remove(dbfile)

    from google.appengine.api import apiproxy_stub_map,datastore_file_stub
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub(app_id, dbfile, '/')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
