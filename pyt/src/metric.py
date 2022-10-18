import json


# this class represents a given metric
class Metric:
    # takes all the required field and then it is possible to convert it to json
    def __init__(self, source, name, identifier_type, instance_id, label, *args, y_axis_side='left'):
        self.content = [source, name, identifier_type, instance_id, *args, {'label': label, 'yAxis': y_axis_side}]

    def get_json(self):
        return json.dumps(self.content)

    def get_array(self):
        return self.content
