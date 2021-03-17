#!/bin/bash
kubectl scale deploy/$1 --replicas=$2
exit 0