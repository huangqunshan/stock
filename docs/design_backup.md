＃ API
## URL: /api/stock_info/list
描述: 根据一批条件筛选出符合条件的股票列表

message StockListRequest {
    // 市值过滤
    optional double minimum_market_value_b = 1 [default=10];
    // 市场标识：A股，美股
    optional string market_place = 2 [default = "us"];
    optional bool is_etf = 3;
    // 股票列表
    repeated string stock_id = 4;
    // 只考虑中概股
    optional bool is_china = 5;
}

message StockListResponse {
    repeated StockItem stock_item = 1;
}

    
## URL: /api/stock_recommend/get
request: StockPolicyItemRequest
response: StockPolicyItemResponse


## URL: /api/stock_recommend/check_history_for_policy 模拟历史数据
request:
    {
        stock_id: "baba",
        policy: $policy,
        进入时间: ...,
    }
response:
    {
        累计收益: xxx,
        累计交易次数： 0，
        具体交易时间列表: [],
    }

## URL: /api/stock_recommend/check_all_policy // 多模型
request:
   ｛
        stock_id: "baba",
        multi_model_merge_list: [ {revert_watch_days:[20: 50%, 55: 50%]}],
        until_date: 20170530, 
    ｝
response:
    {
        best_model: [merge, 3, 7, 20, 50], // 多模型， 增加短期以发现市场巨变?
        best_quit_policy: ["lose_rate": 5%, "reverse_min":20],
        best_enter_policy: ["reverse_min": {20: 5.5% /*return rate*/, 10: 3.4%}],
    }
    

# 需求列表
0. 基础假设
* 训练数据观察期（120天）, 希望跨财报
* 预测最长观察周期 (120天)
* 交易券商给定，手续费固定: 按照ib计算
* 给定入场金额

术语:
 - 股票 stock_id
 - 交易最早起始时间 trade_watch_start_date
 - 具体策略 policy_id

1. 单只股票单个策略: key: (stock_id + trade_watch_start_date + policy_id), 
 
 － 要求:
    - 计算最终收益与百分比win_rate
    - 计算交易次数
    - 有效预测观察天数
    - 有效持仓天数
    - 持仓亏损天数¬
    - 计算手续费
    - 期权费用

    
2. 单个股票多个策略: key: (stock_id + trade_watch_start_date + policy_id), (stock best policy for the day)
  - 给定股票stock_id
  - 给定交易起始时间start_date
  
 - 策略排序，最佳策略靠前 (最终收益, 交易次数，亏损次数)

3. 单个股票在不同的天数的策略稳定性(stock best policy for different days): 
     win_count[stock_id][policy] += 1 if win_rate > 1
     fail_count[stock_id][policy] += 1 if win_rate < 1
     同时计算每个策略在所有天数里分位数的win_rate: 10%, 30%, 50%, 70%, 90%
     win_rate_percent_n[n][stock_id][policy] = ...
最终：
    产出: stock_id + policy的收益的分位数信息。
    产出： 排序依据：win_rate, n = 30, 10;
    
4. 根据stock_id + n% + policy_id (market best policy)
最终: 
   产出：基于3
   all_win_count[policy] += 1 for all stock_id if win_rate > 1
   all_fail_count[policy] += 1 for all stock_id if win_rate < 1
   all_win_rate_percent_n[n][policy] = ...
   同时计算每个策略在所有天数里分位数的win_rate: 10%, 30%, 50%, 70%, 90%
   最终排序依据： all_win_rate, n = 30, 10


    
# 整体策略考虑
* 黑天鹅对买入，卖出时机的影响
* 分批买入次数
*传入id 列表，找出不同时间进入所有的策略。找出每个策略的不同天进入表现。
*训练截止时间， 观察起始时间，每日累计收益
*买入卖出等操作记录
*资金总额考虑
*分批进入策略
*定时进入策略
*定额进入策略
*持有策略：观察周期内不退出

## 复杂策略考虑
关联： 前一天或前几天的某股票升降影响了另外几只股票的表现;
* 策略： 平稳期： 涨就卖， 跌就买
* 策略： 关注开盘半小时， 总是逆向操作