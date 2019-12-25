import pymongo
import sys
import json
import base64


class dbClient:
    def __init__(self, *args, **kwargs):
        self.getDb(*args, **kwargs)

    def dictMerge(self, dict):
        return '&'.join(f'{k}={v}' for k, v in dict.items())

    def getDb(self, settings):
        # 1. Create a MongoDB client
        # 2. Open a connection to Amazon DocumentDB as a replica set
        # 3. Specify the read preference as secondary preferred
        self.params = {
            'dbusername': '',
            'dbpassword': '',
            'dbname': 'someDB',
            'host': '0.0.0.0',
            'port': 27017,
            'tls': 'true',
            'verbose': 'true',
            'aws': {
                'clustername': 'mycluster',
                'node': 'node',
                'serverlocation': 'us-east-1',
                'replicaSet': 'rs0',
                'readPreference': 'secondaryPreferred'
            }
        }
        self.params.update(settings)
        self.dbUsername = self.params['dbusername']
        self.dbPassword = self.params['dbpassword']
        self.dbName = self.params['dbname']
        self.host = self.params['host']
        self.port = self.params['port']
        self.tls = self.params['tls']
        self.verbose = self.params['verbose']
        self.clusterName = self.params['aws']['clustername']
        self.node = self.params['aws']['node']
        self.serverLocation = self.params['aws']['serverlocation']
        self.replicaSet = self.params['aws']['replicaSet']
        self.readPreference = self.params['aws']['readPreference']
        self.isAWS = (self.host.lower() == 'aws')

        request = []
        request.append('mongodb://')
        if self.host.lower() == 'aws':
            request.extend([self.dbUsername, ':', self.dbPassword, '@'])
            self.host = \
                '.'.join([self.clusterName, self.node, self.serverLocation,
                         'docdb', 'amazonaws', 'com'])
            if self.tls.lower() == 'true':
                self.params['aws']['ssl'] = 'true'
                self.params['aws']['ssl_ca_certs'] = \
                    'rds-combined-ca-bundle.pem'
            awsParams = self.params['aws']
            request.extend([self.host, ':', str(self.port), '/'])
            request.extend(['?', self.dictMerge(awsParams)])
        else:
            request.extend([self.host, ':', str(self.port), '/'])
        completeRequest = ''.join(request)
        if self.verbose.lower() == 'true':
            print('[dbClient]: Connecting to DB ['+self.dbName+'] ' +
                  'using the request: ['+completeRequest+']')
        self.connectionHandle = pymongo.MongoClient(completeRequest)
        self.dbHandle = self.connectionHandle.get_database(self.dbName)
        return

    def setTargetCollection(self, col):
        # Specify the collection to be used
        if self.verbose.lower() == 'true':
            print('[dbClient]: Setting collection ['+col+'] as target...')
        self.col = self.dbHandle.get_collection(col)
        return

    def findDoc(self, doc, many=False):
        # Find the document that was previously written
        if self.verbose.lower() == 'true':
            print('[dbClient]: Getting document [' +
                  str(doc).replace('\n', '')+']...')
        if many is True:
            return self.col.find(doc)
        else:
            return self.col.find_one(doc)

    def insertDoc(self, doc, many=False):
        # Insert a single document
        if self.verbose.lower() == 'true':
            print('[dbClient]: Inserting document [' +
                  str(doc).replace('\n', '')+']...')
        if many is True:
            self.col.insert_many(doc)
        else:
            self.col.insert_one(doc)

    def removeDoc(self, doc, many=False):
        # Delete a single document
        if self.verbose.lower() == 'true':
            print('[dbClient]: Deleting document [' +
                  str(doc).replace('\n', '')+']...')
        if many is True:
            self.col.delete_many(doc)
        else:
            self.col.delete_one(doc)

    def closeDB(self):
        # Close the connection
        self.connectionHandle.close()


def decodeAndLoad(source):
    # Loads the settings file `dm-pricing.json`
    return json.loads(base64.b64decode(open(source, 'rb').read()))


def main():
    connectionSettings = decodeAndLoad('dm-pricing-qa.crpt')

    print(connectionSettings)

    # Establish connection through a dbClient client
    #  with the proper conenction settings
    mongoConnection = dbClient(connectionSettings)

    # Sets the collection to `someCollection`
    mongoConnection.setTargetCollection('someCollection')

    # Create single and multiple sample documents
    doc = {'hello': 'Amazon DocumentDB'}
    docs = []
    docs.append({'hello': 'world'})
    docs.append({'hello': 'woorld'})
    docs.append({'hello': 'woorld'})

    # Insert a single document
    mongoConnection.insertDoc(doc)

    # Read a single document
    retreivedDoc = mongoConnection.findDoc(doc)
    print('Response:', str(retreivedDoc).replace('\n', ''))

    # Remove a single document
    mongoConnection.removeDoc(retreivedDoc)

    # Insert multiple documents all at once
    mongoConnection.insertDoc(docs, many=True)

    # Read multiple documents all at once
    mongoConnection.findDoc({"hello": "woorld"}, many=True)

    # Remove multiple documents based on a `filter`
    mongoConnection.removeDoc({"hello": "woorld"}, many=True)

    # Close database
    mongoConnection.closeDB()


if __name__ == '__main__':
    main()
