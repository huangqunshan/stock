# coding=utf8

import json
import logging
import sys
import re


def main():
    stock_list = []
    fields_list = ["name", "cname", "category", "symbol", "mktcap", "pe", "volume", "market"]

    all_fields_list = ["null", "count", "data", "name", "cname", "category", "symbol", "price", "diff", "chg", "preclose", "open", "high", "low",
                       "amplitude", "category_id", "mktcap", "pe", "volume",  "market"]

    for line in sys.stdin.readlines():
        for field in all_fields_list:
            line = re.sub(r"(\W)%s:" % field, r'\1"%s":' % field, line)
        sys.stdout.write(line)
        continue
        decoder = json.JSONDecoder('utf8', strict=False)
        obj = decoder.decode(line)

        # obj = json.loads(line)
        for item in obj["data"]:
            cur_field_list = []
            for field in fields_list:
                cur_field_list.append(item[field])
            stock_list.append(cur_field_list)
    print "\t|\t".join(fields_list)
    for item in stock_list:
        print "\t".join(item)


main()
