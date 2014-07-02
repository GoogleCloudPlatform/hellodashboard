from googleapiclient.discovery import build

class BigQueryClient(object):
    def __init__(self, decorator):
        """Creates the BigQuery client connection"""
        decorated_http = decorator.http()
        self.service = build('bigquery', 'v2', http=decorated_http)
        self.decorator = decorator

    def getTableData(self, project, dataset, table):
        decorated_http = self.decorator.http()
        tablesCollection = self.service.tables()
        request = tablesCollection.get(
            projectId=project,
            datasetId=dataset,
            tableId=table)
        return request.execute(decorated_http)

    def getLastModTime(self, project, dataset, table):
        data = self.getTableData(project, dataset, table)
        if data and 'lastModifiedTime' in data:
            return data['lastModifiedTime']
        else:
            return None

    def Query(self, query, project, timeout_ms=10000):
        query_config = {
            'query': query,
            'timeoutMs': timeout_ms
        }
        decorated_http = self.decorator.http()
        result_json = (self.service.jobs()
                       .query(projectId=project,
                       body=query_config)
                      .execute(decorated_http))
        return result_json
