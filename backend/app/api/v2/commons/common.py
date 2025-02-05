from datetime import datetime
import pandas as pd
from app.services.search import ElasticService


async def getData(start_datetime: datetime, end_datetime: datetime):
    query = {
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "timestamp": {
                            "format": "yyyy-MM-dd HH:mm:ss"
                        }
                    }
                }
            }
        }
    }
    query['query']['bool']['filter']['range']['timestamp']['lte'] = str(end_datetime.replace(microsecond=0))
    query['query']['bool']['filter']['range']['timestamp']['gte'] = str(start_datetime.replace(microsecond=0))

    es = ElasticService()
    response = await es.post(query)
    await es.close()
    tasks = [item['_source'] for item in response["hits"]["hits"]]
    jobs = pd.json_normalize(tasks)

    if len(jobs) == 0:
        return jobs

    cleanJobs = jobs[jobs['platform'] != ""]

    jbs = cleanJobs
    jbs['shortVersion'] = jbs['ocpVersion'].str.slice(0, 4)

    return jbs
