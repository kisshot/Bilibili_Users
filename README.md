# Bilibili_Users
使用Redis,Scrapy,MongoDB实现分布式爬虫，抓取Bilibil用户信息
这个项目是我初学爬虫的练手，同时作为留学申请的素材之一，接下来的几个月我将会逐步完善代码。
项目分为4个阶段：
  阶段1：简单的用户信息抓取，不涉及代理池等反爬虫措施，仅用于熟悉流程
  阶段2：使用scrapy框架完成抓取，连接代理池，cookie池，将结果存储于MongoDB数据库中
  阶段3：在阶段2的基础上实现分布式爬虫，使用redis实现
  阶段4：借助爬取到的数据进行用户资料的分析
