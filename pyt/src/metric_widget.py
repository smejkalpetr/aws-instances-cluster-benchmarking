import json


# represents the whole widget that is sent to aws as a query (in json format)
class MetricWidget:
    data = None
    
    def __init__(self, metrics, name, stat_type='Average'):
        self.metrics = [metric.get_array() for metric in metrics]
        self.view = 'timeSeries'
        self.name = name
        self.stat = stat_type
        self.period = 60
        self.yAxis = {'left': {'min': 0}}
        self.region = 'us-east-1'
        self.timezone = '-0400'
        self.start = '-PT15M'
        self.end = 'P0D'

    def encode_json(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=False,
                          indent=4)
            