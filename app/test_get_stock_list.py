
import time
import urllib2


url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['OlzxjV9ZUfqCsPT0']/US_CategoryService.getList?page=%s&num=60&sort=&asc=0&market=&id="

for page_num in range(1,134):
    f = urllib2.urlopen(url % page_num)
    time.sleep(0.1)
    print f.read()

grep -o 'symbol:"\w*"' stock_list.sina_utf8 |sed -e 's,symbol:,,g' -e 's,",,g' > stocl_list.sina_clean
#http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['OlzxjV9ZUfqCsPT0']/US_CategoryService.getList?page=2&num=60&sort=&asc=0&market=&id=