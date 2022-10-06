#!/bin/bash

# #::: createMetrics.sh :::#
# This script creates some different metrics for measuring the performance of the benchmarks
STARTTIME = 2022-10-06T00:00:00Z
ENDTIME = 2022-10-06T00:10:00Z
PERIOD = 60
LBVALUE = app/my-load-balancer/50dc6c495c0c9188
TGVALUE1 = targetgroup/my-targets/73e2d6bc24d8a067
TGVALUE2 = targetgroup/my-targets/73e2d6bc24d8a068
NAME = AWS/ApplicationELB

# Rule Evaluation
aws cloudwatch get-metric-statistics --namespace $(NAME) \
--metric-name RuleEvaluations --statistics Sum --period $(PERIOD) \
--dimensions Name=LoadBalancer,Value= $(LBVALUE) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

# Request Count
aws cloudwatch get-metric-statistics --namespace $(NAME) \
--metric-name HealthyHostCount --statistics Average  --period $(PERIOD)\
--dimensions Name=LoadBalancer,Value= $(LBVALUE) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

# Consumed LCUs
aws cloudwatch get-metric-statistics --namespace $(NAME)\
--metric-name HealthyHostCount --statistics Average  --period $(PERIOD)\
--dimensions Name=LoadBalancer,Value=$(LBVALUE) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

# Healthy host count
aws cloudwatch get-metric-statistics --namespace $(NAME)\
--metric-name HealthyHostCount --statistics Average  --period $(PERIOD)\
--dimensions Name=LoadBalancer,Value= $(LBVALUE) \
Name=TargetGroup,Value= $(TGVALUE1) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

# Request count per target
aws cloudwatch get-metric-statistics --namespace $(NAME)\
--metric-name HealthyHostCount --statistics Average  --period $(PERIOD)\
--dimensions Name=LoadBalancer,Value= $(LBVALUE) \
Name=TargetGroup,Value=$(TGVALUE1) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

# Target response time
aws cloudwatch get-metric-statistics --namespace $(NAME)\
--metric-name HealthyHostCount --statistics Average  --period $(PERIOD)\
--dimensions Name=LoadBalancer,Value=$(LBVALUE) \
Name=TargetGroup,Value= $(TGVALUE1) \
--start-time $(STARTTIME) --end-time $(ENDTIME)

