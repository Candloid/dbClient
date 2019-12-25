# dbClient
MongoDB client to connect to AWS DocumentDB

## Instantiate a connection
```python
connectionSettings = {
    "dbusername": "someUser",
    "dbpassword": "somePassword",
    "dbname": "someDB",
    "host": "aws",
    "port": 27017,
    "tls": "False",
    "verbose": "True",
    "aws": {
        "clustername": "cluster",
        "node": "node",
        "serverlocation": "us-west-2",
        "replicaSet": "rs0",
        "readPreference": "secondaryPreferred"
    }
}

mongoConnection = dbClient(connectionSettings)
```

## Establish connection through a dbClient client with the proper conenction settings
```python
mongoConnection = dbClient(connectionSettings)
```

## Sets the collection to `someCollection`
```python
mongoConnection.setTargetCollection('someCollection')
```

## Insert a single document
```python
pythonmongoConnection.insertDoc({'hello': 'world'})
```

## Read a single document
```python
retreivedDoc = mongoConnection.findDoc({'hello': 'world'})
```

## Remove a single document
```python
mongoConnection.removeDoc(retreivedDoc)
```

## Insert multiple documents all at once
```python
mongoConnection.insertDoc(docs, many=True)
```

## Read multiple documents all at once
```python
mongoConnection.findDoc({"hello": "woorld"}, many=True)
```

## Remove multiple documents based on a `filter`
```python
mongoConnection.removeDoc({"hello": "woorld"}, many=True)
```

## Close database
```python
mongoConnection.closeDB()
```
