#!/usr/bin/env bash
protoc --proto_path=. --python_out=. proto/stock_info.proto
protoc --proto_path=. --python_out=. proto/policy.proto 
protoc --proto_path=. --python_out=. proto/person.proto 
