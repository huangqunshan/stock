#!/usr/bin/env bash

sh generate_proto_py.sh && python main_train.py --quick_policy $1