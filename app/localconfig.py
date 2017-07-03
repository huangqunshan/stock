# coding=utf8

import datetime
from datetime_util import DatetimeUtil
from proto.policy_pb2 import Policy


cash_taken_in = 30000
max_train_watch_days = 0
max_predict_watch_days = 0
max_watch_jump_times = 10
DEFAULT_TIMEOUT_SECONDS = 2.0
EXPIRE_AFTER_MS = 10000
EXPIRE_AFTER_DAYS = 100
POSITION_PERCENT_LIST = range(0, 100+1, 10)
end_date_str = DatetimeUtil.to_datetime_str(datetime.datetime.now())


# best policy fix for improve train speed

# buy_days_watch:15	2-5-8-9:	1.19510914734 # 14.192, 1.02821984262 # 8.4, 0.895496480751 # 2.92, 0.764960191049 # 1.811
# buy_days_watch:10	2-5-8-9:	1.20854553604 # 17.122, 1.02189637158 # 10.4, 0.8855222122 # 3.8, 0.722699301807 # 1.93
# buy_days_watch:20	2-5-8-9:	1.16628610024 # 12.32, 1.02160154956 # 7.2, 0.904542472462 # 2.42, 0.769281673976 # 1.189
# buy_days_watch:5	2-5-8-9:	1.2031678982 # 23.874, 1.02081145021 # 13.75, 0.848808013158 # 5.36, 0.665902869118 # 2.426

# buy_days_watch:10	2|1.27618183573|3.0	5|1.03041774929|0.0	8|1.0|0.0	9|0.962719134448|0.0
# buy_days_watch:15	2|1.2081060447|2.0	5|1.00332401595|0.0	8|1.0|0.0	9|0.989865829823|0.0
# buy_days_watch:30	2|1.0564845995|1.0	5|1.0|0.0	8|1.0|0.0	9|0.994694594694|0.0
# buy_days_watch:20	2|1.12920368388|1.0	5|1.0|0.0	8|1.0|0.0	9|0.988245656509|0.0

BUY_WATCH_DAYS_LIST = [15]
# sell_days_watch:15	2-5-8-9:	1.23013866919 # 14.912, 1.04704621872 # 8.44, 0.891200242997 # 3.0, 0.733736507942 # 1.741
# sell_days_watch:20	2-5-8-9:	1.22479592739 # 13.204, 1.04063553463 # 7.5, 0.897240429646 # 2.468, 0.730709881747 # 1.219
# sell_days_watch:10	2-5-8-9:	1.17930207727 # 17.044, 1.02475195877 # 9.8, 0.877468725376 # 3.92, 0.684441354771 # 1.93
# sell_days_watch:5	2-5-8-9:	1.11310061124 # 23.4, 0.99330735526 # 13.82, 0.860888243394 # 4.88, 0.682299132134 # 2.24

# sell_days_watch:10	2|1.12277182673|3.0	5|1.0|0.0	8|1.0|0.0	9|0.976373102625|0.0
# sell_days_watch:30	2|1.22019602608|1.0	5|1.0|0.0	8|1.0|0.0	9|0.994002807143|0.0
# sell_days_watch:15	2|1.1555880782|2.0	5|1.0|0.0	8|1.0|0.0	9|0.983874971044|0.0
# sell_days_watch:20	2|1.17920895004|1.0	5|1.0|0.0	8|1.0|0.0	9|0.991481424755|0.0

SELL_WATCH_DAYS_LIST = [15]



DAYS_HOLD_FOR_SALE_LIST = [5]



# buy_percent_n:20	2-5-8-10:	1.20428389305 # 12.808, 1.04677392881 # 7.9, 0.921295918214 # 3.12, 0.785876241192 # 2.0
# buy_percent_n:30	2-5-8-10:	1.20617618691 # 14.0, 1.04500483541 # 8.725, 0.901410365332 # 3.72, 0.757108894934 # 2.0

# buy_percent_n:30	2|1.14214064233|2.0	5|1.0|0.0	8|0.98935350354|0.0	9|0.806162493922|0.0
# buy_percent_n:50	2|1.1643599906|3.0	5|1.0|0.0	8|0.978710149621|0.0	9|0.776383016797|0.0:%s

# 50 > 40, 50 > 60
BUY_PRICE_PERCENT_LIST = range(50, 50 + 1, 10)

# sell_percent_n:110	2-5-8-9:	1.26625731137 # 11.2, 1.13306259364 # 7.2, 1.04533893279 # 3.0, 1.02193602462 # 2.0
# sell_percent_n:100	2-5-8-9:	1.26625731137 # 11.2, 1.13306259364 # 7.2, 1.04533893279 # 3.0, 1.02193602462 # 2.0
# sell_percent_n:80	2-5-8-9:	1.26102344763 # 14.0, 1.12368146811 # 8.8, 1.04223373156 # 3.8, 1.01569045808 # 2.0
# sell_percent_n:90	2-5-8-9:	1.26542120237 # 12.2, 1.12301105862 # 8.0, 1.04192526162 # 3.72, 1.01968853688 # 2.0
# sell_percent_n:70	2-5-8-9:	1.23610520233 # 14.76, 1.12165929586 # 9.4, 1.04262850752 # 4.08, 1.01869211194 # 2.48
# sell_percent_n:60	2-5-8-9:	1.21051657253 # 15.44, 1.1026040635 # 9.9, 1.03802631457 # 4.08, 1.01353593443 # 2.8
# sell_percent_n:50	2-5-8-9:	1.20158110578 # 16.18, 1.08226989692 # 10.3, 1.02682962936 # 4.08, 1.00627234815 # 2.8

# sell_percent_n:50	2|1.14604444506|3.0	5|1.0|0.0	8|0.983470277419|0.0	9|0.787220679507|0.0
# sell_percent_n:70	2|1.16121659902|2.0	5|1.0|0.0	8|0.98804124582|0.0	9|0.791267569279|0.0

SELL_PRICE_PERCENT_LIST = range(50, 50 + 1, 10)

# buy_mode:1; 2 - 5 - 8 - 10:    1.20042430959  # 14.92, 1.04264026959 # 9.25, 0.905355531836 # 3.892, 0.0261296704281 # 0.0
# buy_mode:3; 2 - 5 - 8 - 10:    1.20547857769  # 20.434, 1.02425980384 # 12.16, 0.8800411176 # 5.0, 0.0215538388489 # 0.0
BUY_MODE_LIST = [Policy.TradePolicy.Percent.LOW]

# sell_mode:2; 2 - 5 - 8 - 10:    1.21805349502  # 14.84, 1.04524164974 # 9.225, 0.896557619738 # 3.88, 0.0215538388489 # 0.0
# sell_mode:3; 2 - 5 - 8 - 10:    1.16409161087  # 20.48, 1.02165842369 # 12.46, 0.883413927914 # 5.028, 0.0221897851161 # 0.0
SELL_MODE_LIST = [Policy.TradePolicy.Percent.HIGH]

# 亏损时采用当天最低价结算
# loss_thousandth:990	2-5-8-9:	1.19076378091 # 13.0, 1.05403091586 # 8.3, 0.92836392508 # 3.6, 0.786737482675 # 2.0
# loss_thousandth:90	2-5-8-9:	1.12389635797 # 17.24, 0.988076539468 # 11.0, 0.709886877256 # 4.6, 0.450250413156 # 2.66
# loss_thousandth:70	2-5-8-9:	1.10098349753 # 19.08, 0.954325797968 # 12.0, 0.673595279022 # 4.7, 0.387051076421 # 2.9
# loss_thousandth:50	2-5-8-9:	1.06228667569 # 23.0, 0.906782936813 # 13.9, 0.592815592142 # 5.7, 0.323292285201 # 3.0
# loss_thousandth:30	2-5-8-9:	1.00786199591 # 28.78, 0.83316303845 # 17.5, 0.520302331885 # 6.86, 0.241835300511 # 4.0
# loss_thousandth:10	2-5-8-9:	0.916745495217 # 38.12, 0.726997007631 # 24.3, 0.415436638131 # 9.66, 0.206007871194 # 5.12
# 亏损时采用乐观亏损限价结算
# loss_thousandth:990	2-5-8-9:	1.19076378091 # 13.0, 1.05403091586 # 8.3, 0.92836392508 # 3.6, 0.786737482675 # 2.0
# loss_thousandth:90	2-5-8-9:	1.15440990512 # 15.84, 1.01682631063 # 10.0, 0.832401623145 # 3.76, 0.66510656362 # 2.0
# loss_thousandth:70	2-5-8-9:	1.13579086111 # 16.4, 1.00624951176 # 10.2, 0.824617164323 # 3.8, 0.665041861354 # 2.0
# loss_thousandth:10	2-5-8-9:	1.11206508416 # 21.68, 1.00312269245 # 12.5, 0.89701258595 # 5.0, 0.773352594126 # 2.83
# loss_thousandth:50	2-5-8-9:	1.12048712551 # 18.34, 1.002961264 # 11.0, 0.818331702732 # 4.4, 0.675737629067 # 2.0
# loss_thousandth:30	2-5-8-9:	1.1068305836 # 21.0, 0.994854041732 # 12.0, 0.84103462556 # 4.7, 0.670549122535 # 2.8

# loss_stop_thousandth:900	2-5-8-9:	1.34036059876 # 8.904, 1.09842756675 # 3.0, 0.937667478263 # 0.9, 0.724961949606 # 0.0
# loss_stop_thousandth:500	2-5-8-9:	1.34036059876 # 9.0, 1.09842756675 # 3.3, 0.935952731851 # 1.0, 0.687904312898 # 0.0
# loss_stop_thousandth:90	2-5-8-9:	1.2160927858 # 15.696, 1.03172633938 # 6.97, 0.822711139387 # 2.0, 0.658555177763 # 0.81
# loss_stop_thousandth:50	2-5-8-9:	1.16396648997 # 18.4, 1.00514265302 # 8.5, 0.807983797907 # 2.824, 0.621501427166 # 0.956

# LOSS_STOP_THOUSANDTH_LIST = range(10, 90+1, 10) + [990]
LOSS_STOP_THOUSANDTH_LIST = [100, 990]

# sell_percent_n:80	2-5-8-9:	1.19076378091 # 13.0, 1.05403091586 # 8.3, 0.92836392508 # 3.6, 0.786737482675 # 2.0
# sell_profit_thousandth_n:1000	2-5-8-9:	1.5010364146 # 0.0, 1.12682739029 # 0.0, 0.927094149429 # 0.0, 0.712499716577 # 0.0
# sell_profit_thousandth_n:200	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73
# sell_profit_thousandth_n:25	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73
# sell_profit_thousandth_n:45	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73
# sell_profit_thousandth_n:5	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73
# sell_profit_thousandth_n:65	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73
# sell_profit_thousandth_n:85	2-5-8-9:	1.0604950619 # 21.6, 1.00374652301 # 11.45, 0.917648813809 # 4.96, 0.715426493074 # 2.73


# sell_profit_thousandth_n:200	2-5-8-9:	1.43970918457 # 5.944, 1.09809752083 # 1.45, 0.866355942069 # 0.0, 0.649154260983 # 0.0
# sell_profit_thousandth_n:100	2-5-8-9:	1.36827897795 # 9.056, 1.08808726417 # 3.0, 0.875540391053 # 1.0, 0.682285898655 # 0.0
# sell_profit_thousandth_n:70	2-5-8-9:	1.30185530975 # 10.404, 1.06867575741 # 4.0, 0.873792009823 # 1.0, 0.688332386247 # 0.0
# sell_profit_thousandth_n:60	2-5-8-9:	1.28096832897 # 10.96, 1.06480182194 # 4.305, 0.864789814787 # 1.174, 0.693480990739 # 0.0
# sell_profit_thousandth_n:40	2-5-8-9:	1.22986507757 # 12.852, 1.06000973145 # 5.6, 0.84370835014 # 1.96, 0.672369486568 # 0.781
# sell_profit_thousandth_n:30	2-5-8-9:	1.20590738361 # 14.22, 1.05856928215 # 6.295, 0.818411912739 # 2.0, 0.645315849475 # 0.93
# sell_profit_thousandth_n:50	2-5-8-9:	1.25618761386 # 11.924, 1.05825366075 # 4.9, 0.856458764735 # 1.42, 0.672574552404 # 0.0
# sell_profit_thousandth_n:20	2-5-8-9:	1.16060005121 # 16.52, 1.03285856657 # 7.65, 0.809441743325 # 2.498, 0.633022650948 # 1.0
# sell_profit_thousandth_n:10	2-5-8-9:	1.11877784526 # 20.526, 1.00805316199 # 10.05, 0.800152829283 # 3.0, 0.628971664919 # 1.951

# SELL_PROFIT_THOUSANDTH_LIST = range(10, 100+1, 10) + [200, 1000]
# SELL_PROFIT_THOUSANDTH_LIST = range(10, 150, 10) + [200, 1000]
SELL_PROFIT_THOUSANDTH_LIST = []


# buy_growth:-1	2|1.39824154992|7.0	5|1.07432906313|1.0	8|0.916727451392|0.0	9|0.734182097445|0.0
# buy_growth:60	2|1.30646794751|4.0	5|1.05485563502|1.0	8|0.956405672571|0.0	9|0.775182959862|0.0
# buy_growth:50	2|1.2996137245|5.0	5|1.04051441788|1.0	8|0.916443345775|0.0	9|0.709671263296|0.0
# buy_growth:40	2|1.28197405849|5.0	5|1.02324041469|1.0	8|0.914381169438|0.0	9|0.748005172722|0.0
# buy_growth:30	2|1.2794214377|4.0	5|1.02048546004|1.0	8|0.927510344754|0.0	9|0.751776313067|0.0
# buy_growth:20	2|1.20056988372|3.0	5|1.00546514665|1.0	8|0.94170535903|0.0	9|0.772035426815|0.0
# buy_growth:10	2|1.09015217942|1.0	5|1.0|0.0	8|0.999720735412|0.0	9|0.877020965932|0.0
# buy_growth:0	2|1.0|0.0	5|1.0|0.0	8|1.0|0.0	9|1.0|0.0
# buy_growth:70	2|1.18104924715|2.0	5|1.0|0.0	8|0.982036816425|0.0	9|0.887595657281|0.0
# buy_growth:90	2|1.0|0.0	5|1.0|0.0	8|1.0|0.0	9|1.0|0.0
# buy_growth:100	2|1.0|0.0	5|1.0|0.0	8|1.0|0.0	9|1.0|0.0
# buy_growth:80	2|1.0|0.0	5|1.0|0.0	8|1.0|0.0	9|0.963097412191|0.0


# policy_group_buy_growth:60	2|1.4883546852|2.0	5|1.24570273818|0.0	8|1.0008812183|0.0	9|0.965364615616|0.0
# policy_group_buy_growth:50	2|1.55567495928|2.0	5|1.23497396179|0.0	8|1.0|0.0	9|0.966109191994|0.0
# policy_group_buy_growth:40	2|1.51967278354|2.0	5|1.19028755597|0.0	8|1.00395202058|0.0	9|0.970898749328|0.0
# policy_group_buy_growth:30	2|1.41735065052|2.0	5|1.11130968608|0.0	8|1.0|0.0	9|0.975585208841|0.0
# weak signal: 30
# strong signal: 60
# 20160101-20160630,
# buy_growth:60	2|1.09328749252|0.0	5|1.0|0.0	8|0.951283809971|0.0	9|0.86995866508|0.0
# buy_growth:50	2|1.01188010102|1.0	5|0.977810342191|0.0	8|0.876620082362|0.0	9|0.846202269364|0.0
# buy_growth:40	2|1.03671499191|1.0	5|0.97135708436|0.0	8|0.859918035342|0.0	9|0.839724607089|0.0

BUY_TREND_GROW_PERCENT_LIST = range(40, 60+1, 10)


# sell_growth:10	2|1.28491791864|0.0	5|1.0|0.0	8|0.994491024966|0.0	9|0.771973574354|0.0
# sell_growth:20	2|1.23969357188|1.0	5|1.0|0.0	8|0.988016293489|0.0	9|0.788675932739|0.0
# sell_growth:30	2|1.15339787064|3.0	5|1.0|0.0	8|0.988016293489|0.0	9|0.82434876289|0.0
# sell_growth:50	2|1.0661622119|5.3	5|1.0|1.0	8|0.971301054141|0.0	9|0.79815586773|0.0
# sell_growth:40	2|1.10893138567|4.6	5|1.0|1.0	8|0.980603324818|0.0	9|0.840017421358|0.0
# sell_growth:60	2|1.07183731465|5.0	5|1.0|1.0	8|0.97329935858|0.0	9|0.762652987399|0.0
# sell_growth:0	2|1.29164974884|0.0	5|1.0|0.0	8|0.994491024966|0.0	9|0.765337356372|0.0
# sell_growth:-1	2|1.0537570337|7.0	5|1.0|1.0	8|0.981064571213|0.0	9|0.88902008804|0.0
# sell_growth:70	2|1.10448962376|4.0	5|1.0|1.0	8|0.979716959166|0.0	9|0.786927268201|0.0
# sell_growth:90	2|1.2523584357|1.0	5|1.0|0.0	8|0.993072216639|0.0	9|0.767020894042|0.0
# sell_growth:80	2|1.1702749187|2.6	5|1.0|0.0	8|0.993954142768|0.0	9|0.776849344576|0.0
# sell_growth:100	2|1.25440069064|0.0	5|1.0|0.0	8|0.99962955005|0.0	9|0.765337356372|0.0


# policy_group_sell_growth:0	2|1.54233824608|0.0	5|1.298088581|0.0	8|1.00502296667|0.0	9|0.995674664499|0.0
# policy_group_sell_growth:10	2|1.52290975436|0.0	5|1.27683210244|0.0	8|1.00502296667|0.0	9|0.995674664499|0.0
# policy_group_sell_growth:100	2|1.51897215737|1.0	5|1.22551229448|0.0	8|1.00498647871|0.0	9|0.995674664499|0.0
# policy_group_sell_growth:90	2|1.52266613266|2.0	5|1.21835517546|0.0	8|1.01111871991|0.0	9|1.0|0.0
# policy_group_sell_growth:20	2|1.53339341428|2.0	5|1.20480769048|1.0	8|1.0|0.0	9|0.961355056852|0.0
# policy_group_sell_growth:80	2|1.43880068682|3.0	5|1.11701674426|2.0	8|1.0|0.6	9|0.962230864746|0.0
# policy_group_sell_growth:30	2|1.41981945139|5.0	5|1.11340517293|3.0	8|1.0|0.12	9|0.976346263342|0.0
# weak signal: 30, 80
# 20160101-20160630,10,20,30,40, 80, 90,90,100
# sell_growth:30	2|1.06643949694|2.0	5|1.0|1.0	8|0.883547557092|0.0	9|0.85361084507|0.0
# sell_growth:40	2|1.08578629152|3.0	5|1.0|1.0	8|0.944407085988|0.0	9|0.897487287998|0.0
# sell_growth:80	2|1.09328749252|1.0	5|0.998825822306|0.0	8|0.911746575572|0.0	9|0.857058510722|0.0
# sell_growth:60	2|1.01259366246|3.0	5|0.982575916995|1.0	8|0.874156373354|0.0	9|0.85759015245|0.0
# sell_growth:10	2|1.04966712522|0.0	5|0.978834871005|0.0	8|0.872579006318|0.0	9|0.836109860532|0.0
# sell_growth:20	2|1.02852095687|1.0	5|0.978834871005|0.0	8|0.864197648947|0.0	9|0.833876145377|0.0
# sell_growth:0	2|1.04966712522|0.0	5|0.978834871005|0.0	8|0.86995866508|0.0	9|0.84954129066|0.0
# sell_growth:90	2|1.04966712522|0.0	5|0.978834871005|0.0	8|0.86995866508|0.0	9|0.84954129066|0.0
# sell_growth:100	2|1.04966712522|0.0	5|0.978834871005|0.0	8|0.86995866508|0.0	9|0.84954129066|0.0
# sell_growth:50	2|1.00081449273|3.0	5|0.97705829169|1.0	8|0.874886337431|0.0	9|0.852500640412|0.0
# sell_growth:70	2|1.00265790532|2.0	5|0.96976301765|1.0	8|0.872515982305|0.0	9|0.857058510722|0.0
SELL_TREND_GROW_RECENT_LIST = range(0, 40+1, 10) + range(80, 100+1, 10)


# fin_stock = open('stock_list.easy')

fin_stock = open('stock_list.easy3')
select_stock_name_list = fin_stock.read().split('\n')
fin_stock.close()


# SELL_TREND_GROW_RECENT_LIST = range(0, 100+1, 10)

# select_stock_name_list = ["BABA", "JD", "WB", "AMZN", "BIDU", "MSFT", "FB", "GOOGL", "NTES", "TSLA", "MOMO",  "NVDA", "AAPL",
#                           "SPY", "QQQ", "IWM", "IWV"]
# start_date_str = "20150101"
start_date_str = "20160101"
end_date_str = "20160630"

#
# select_stock_name_list = ["BABA"]
# DAYS_HOLD_FOR_SALE_LIST = [30]
# start_date_str = "20170101"

