# 说明：

最终目的：把58同城租房信息在地图上标注出来。

http://cdn.bizha.top/echarts/zufang_bengbu.html

![Snipaste_2023-01-28_20-43-18](https://images.bizha.top/picgo/202301282043833.png)



- 爬虫：

春节期间时间充足，用`selenium`做的爬虫，并且`time.sleep()`设置的非常保守。**爬取速度非常的慢**！验证码几乎不会触发。

- 数据处理思路：

抓取租房信息的`BD-09`坐标，手动转换为`GCJ-02`坐标，用`folium`在地图上标注出来。