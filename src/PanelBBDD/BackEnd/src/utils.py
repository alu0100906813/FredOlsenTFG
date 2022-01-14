
def parseQuery(queryResult):
  results = []
  for table in queryResult:
    for record in table.records:
      results.append((str(record.get_time().time()), record.get_value()))
  return results


def sampleQuery(topic, time = 5, bucket = 'Ships'):
  return 'from(bucket: "{bucket}")\
  |> range(start: -{time}m)\
  |> filter(fn: (r) => r["_measurement"] == "{topic}")\
  |> yield(name: "last")'.format(bucket=bucket, time=time, topic=topic)