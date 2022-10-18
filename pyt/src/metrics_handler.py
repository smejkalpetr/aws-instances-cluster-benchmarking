import os

import boto3

from pathlib import Path

import src.constants
import src.metric_widget
import src.metric


# collects methods used to handle cloud watch metrics
class CloudWatchMetricsHandler:

    constants = src.constants.Constants
    client = boto3.client('cloudwatch')

    def __init__(self, instance_ids, elb_id, tg_ids):
        self.instance_ids = instance_ids
        self.elb_id = elb_id
        self.tg_ids = tg_ids

    # make query for metrics about a single instance and saves them to output directory
    def get_metrics_for_instance(self, instance_id, output_dir):
        chosen_metrics = [
            'CPUUtilization',
            'NetworkIn',
            'NetworkOut',
            'NetworkPacketsIn',
            'NetworkPacketsOut'
        ]

        for metric in chosen_metrics:
            widget = src.metric_widget.MetricWidget(
                [
                    src.metric.Metric(
                        'AWS/EC2',
                        metric,
                        'InstanceId',
                        instance_id,
                        metric
                    )
                ],
                f'Result of {metric} metric.'
            )

            path = os.path.join(output_dir, f'{metric}.png')
            self.get_graph_for_metric(widget, path)

    # gets metrics for all possible instances and saves the results to the output repository
    def get_metrics_for_instances(self):
        for instance_id in self.instance_ids:
            instance_dir = os.path.join(self.constants.VM_OUTPUT_DIR, instance_id)
            Path(instance_dir).mkdir(parents=True, exist_ok=True)

            self.get_metrics_for_instance(instance_id, instance_dir)

    # make a query to get metrics about the one elb and saves them to output directory
    def get_metrics_for_elb(self):
        chosen_metrics = [
            'ConsumedLCUs',
            'RuleEvaluations',
            'TargetResponseTime',
            'RequestCount'
        ]

        Path(self.constants.ELB_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

        for metric in chosen_metrics:
            widget = src.metric_widget.MetricWidget(
                [
                    src.metric.Metric(
                        'AWS/ApplicationELB',
                        metric,
                        'LoadBalancer',
                        self.elb_id,
                        metric
                    )
                ],
                f'Result of {metric} metric.'
            )

            path = os.path.join(self.constants.ELB_OUTPUT_DIR, f'{metric}.png')
            self.get_graph_for_metric(widget, path)

    # make a query to get metrics about the both target groups and saves them to the output directory
    def get_target_groups_metrics(self):
        chosen_metrics = [
            'RequestCount',
            'RequestCountPerTarget',
            'TargetResponseTime'
        ]

        for tg_id in self.tg_ids:
            dir_path = f'{self.constants.TG_OUTPUT_DIR}/{tg_id}'
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            for metric in chosen_metrics:
                widget = src.metric_widget.MetricWidget(
                    [
                        src.metric.Metric(
                            'AWS/ApplicationELB',
                            metric,
                            'TargetGroup',
                            tg_id,
                            metric,
                            'AWS/ApplicationELB',
                            self.elb_id
                        )
                    ],
                    f'Result of {metric} metric.'
                )

                path = os.path.join(dir_path, f'{metric}.png')
                self.get_graph_for_metric(widget, path)

    # this method calls the aws function (image widget) to get a graph in png
    # format based on a give query (json encoded widget)
    def get_graph_for_metric(self, widget, dest_path):
        client = boto3.client('cloudwatch')

        response = client.get_metric_widget_image(
            MetricWidget=widget.encode_json(),
            OutputFormat='png'
        )

        with open(dest_path, "wb") as file:
            file.write(response['MetricWidgetImage'])
