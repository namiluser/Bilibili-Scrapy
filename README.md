Scrapy文档

简介

本项目中包含一个CrawlSpider类的子类MdtvSpider。CrawlSpider是Spider类的一个派生类，Spider类的设计原则是只爬取start_url列表中的网页，而CrawlSpider类定义了一些规则（rule）来提供方便的机制来跟踪链接，从而更适合爬取网页和跟踪链接的任务。


在MdtvSpider类中，基于selenium技术创建了一个浏览器对象（注意，本项目使用的是114版本的Chrome浏览器驱动程序，如果在本机上运行项目时本机上的Chrome浏览器版本不兼容，可能导致项目无法正常启动）。还设置了相关参数来防止检测，处理SSL证书错误问题，以及将加载策略设置为“none”。


start_urls设置为"https://www.bilibili.com/v/douga/mad"，提取器将提取此页面中所有视频的URL。回调函数设置为parse_video，parse_video函数使用基于Xpath的解析方法来获取每个视频的名称、点赞量、播放量、弹幕数、投币数、收藏量和转发量。然后将解析的数据提交到管道DtvPipeline中。


项（Items）

声明和创建了以下项（Items）：



Likes：表示点赞数量。

Playback_volume：表示播放量。

Number_of_barrages：表示弹幕数量。

Number_of_coins_invested：表示投币数量。

Collection_volume：表示收藏量。

Forwarding_volume：表示转发量。

title：表示视频的标题。


中间件（Middlewares）

在下载中间件中，将scrapy框架默认对URL发起请求返回的页面数据替换为MdtvSpider类中声明的浏览器对象访问的页面数据。这样做是为了实现Bilibili的登录功能，防止未登录无法访问目标页面的内容。登录过程是基于手动扫码登录实现的，并且设置了显式的等待时间，只有登录成功后浏览器对象才会继续后续操作。


此外，登录成功后，浏览器对象还会自动滚动页面，实现视频数据的懒加载。


每次访问页面时，还会设置一个随机等待时间，防止时间过短导致无法获取页面数据，还可以防止因访问频率过快被检测为恶意程序。


管道（Pipelines）

创建了一个名为DtvPipeline的管道类，用于将解析的数据存储在本地的CSV文件中。每次项目启动后抓取的视频数据不会覆盖原有数据。


设置（Settings）

在项目的设置中进行了以下设置：



USER_AGENT：设置用户代理。

ROBOTSTXT_OBEY：指定是否遵循robots.txt协议。

LOG_LEVEL：设置日志级别为仅显示错误信息。

DOWNLOADER_MIDDLEWARES：启用下载中间件。

ITEM_PIPELINES：启用DtvPipeline管道。


数据分析

数据预处理

将点赞量、播放量、投币数、转发数、收藏数从字符串类型转换为整数类型。例如，将"13万"转换为130000。此外，原始网页当转发数和投币数为0时显示为"分享"和"投币"，此时需要将其转换为0。


数据分析

分析CSV文件中各列的最大值、最小值、中位数、峰度、偏度、平均值和方差，以及各列之间的相关系数。
