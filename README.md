# Bilibili_Users
使用Redis,Scrapy,MongoDB实现分布式爬虫，抓取Bilibil用户信息
这个项目是我初学爬虫的应用，接下来的几个月我将会逐步完善代码。
## 项目分为4个阶段：
**阶段1：简单的用户信息抓取，不涉及代理池等反爬虫措施，仅用于熟悉流程 \
阶段2：使用scrapy框架完成抓取，连接代理池，cookie池，将结果存储于MongoDB数据库中 \
阶段3：在阶段2的基础上实现分布式爬虫，使用redis实现 \
阶段4：借助爬取到的数据进行用户资料的分析** 
## 文件介绍
* **第一阶段暂存**： \
抓取用户信息，config文件为MongoDB配置文件，user_agents为User-Agent选择文件 \
这个用户信息———>这个用户关注者有谁———>这个用户的关注者信息———>关注者的关注者有谁———>关注者的关注者的个人信息 \
循环抓取，由用户得到关注者再得到关注者的关注者，循环往复 \
连接代理池@jhao104/proxy_pool，信息存储到MongoDB中 
* **第二阶段暂存**： \
原理同上，使用scrapy框架 \
bilitest为核心程序，抓取每个人的姓名和性别信息等，以及他的关注数、粉丝数，实现了MongoDB存储，并且不会存储重复信息，加入了useragent，代理池连接成功，有两种代理连接方式，一种是连接本地setting文件中的代理，另一种是连接api@jhao104/proxy_pool。后续会加上MySQL存储。取得一个人的信息后就会去拿到他的关注者和粉丝的信息，进入循环
* **第三阶段暂存**： \
使用scrapy-redis框架 \
biliredis为核心程序，分布式程序，目前在本地运行成功，requests队列存入了redis数据库中

* **统计结果**： \
![level](https://github.com/kisshot/Bilibili_Users/blob/master/images/level.png)

