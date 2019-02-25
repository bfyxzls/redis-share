<!-- $theme: gaia -->
<!-- page_number: true -->

Redis实践
===


---

# 1、Redis简介

- 开源的,性能强劲(10w QPS)的内存数据库
- 非关系型 键/值 存储
- 支持多种复杂数据类型
- 数据持久化支持
- 高可用、易伸缩
---

# 2、基础数据类型

- Strings
- Lists 
- Sets
- Sorted Sets
- Hashes

---

# 2.1、Strings

|命令|描述
|:-:|:-:
|SET/GET|设置/获取键值
|MSET/MGET|批量设置/获取键值
|INCR/DECR(BY)|将存储的数值增加(减少)1或者指定数
|APPEND |字符串追加
|SETNX*|KEY不存在时才设置

```
SET key value [EX seconds]  [NX]  ==>>  SETNX
```

---

# 2.2、Lists
|命令|描述
|:-:|:-:
|LPUSH/RPUSH(X)|将一个或多个值插入列表的左/右侧
|LREM|移除列表中指定数量的某元素
|LLEN|返回列表长度
|LINDEX|返回列表中某下标的元素
|LPOP/RPOP|移除并返回列表左/右侧的元素

---

# 2.3、Sets
|命令|描述
|:-:|:-:
|SADD|将一个或多个元素加入到集合中
|SISMEMBER|返回元素是否存在于集合中
|SRANDMEMBER |随机返回N个集合中的元素
|SREM|移除集合中的指定元素
|SCARD|返回集合中元素的数量

---

# 2.4、Sorted Sets
|命令|描述
|:-:|:-:
|ZADD|将一个或多个元素指定分值添加到有序集合中
|ZSCORE|返回元素是在集合中的分值
|ZCARD|返回集合中元素的数量
|ZRANGE/ZREVRANGE|正向/逆向返回有续集指定区间内的元素
|ZREM|删除集合指定成员

---

# 2.5、Hashes
|命令|描述
|:-:|:-:
|HSET(NX)|向哈希表中保存指定值
|HGET|取得哈希表中指定key的值
|HDEL|删除哈希表中的一个或多个指定域	
|HEXISTS|检查给定域是否存在于哈希表当中。
|HINCRBY|为哈希表中指定域增加或减少指定值

---

# 3、其它数据类型
- Bitmaps ： *字符串当做二进制位操作:0000001101*
- HyperLogLog(2.8.9)
  - *可以接受多个元素作为输入，并给出输入元素的基数估算值*
  - [1,2,3,4,4,5] 基数 = 5 
  - *只需要12K内存，在标准误差0.81%的前提下，能够统计2^64个数据*
- Geo(3.2.0)

---

# 4、Redis命令
- 普通命令
	- Cluster、Connection、Strings等15个命令组
	- info、set、get等200多条命令
- 危险命令
	- keys、flushdb、flushall
	- rename-command 将危险命令改名或直接禁用
---

# 5、Redis事务
- 命令：multi、watch、exec
- 事务块内的**多条命令**会按照先后顺序被放进一个队列当中，最后由 exec 命令原子性(atomic)地执行。
- 集群环境慎用

``` java
public void flashSell() {
    ops.watch(key);
    ops.multi();
    ops.decr();
    //返回事务内所有命令的结果,nil说明操作被打断   
    ops.exec(); 
}    
```

---
# 6、Lua脚本
- 高效的轻量级脚本语言
- 减少网络开销，减少网络往返的延时
- 增强复用性
- 集群环慎用

---
# 7、持久化

|RDB|AOF
|:-:|:-:
|全量，一次保存整个数据库|增量，一次保存一条命令
|保存时间间隔较长|保存时间间隔默认1秒钟
|数据还原速度快|相对慢，冗余命令越多越慢	
|SAVE阻塞服务，BGSAVE不阻塞|不阻塞
|更适合数据备份|更适合保存数据

---

# 8、缓存设计


---

## 8.1、只缓存热数据

*对于冷数据而言，读取频率低，大部分数据可能还没有再次访问到就已经被挤出内存，不仅占用内存，而且价值不大。*

*对于热点数据，读取频率高。如果不做缓存，给数据库造成很大的压力，可能被击穿。*

---
### 8.2、巧用Hash

- Strings:
  - set user:name 'andy'
  - set user:age 20
  - set user:dept 'tech'
  - set user:address 'beijing'

- Hashes:
  - hset user name 'andy'
  - hset user age 20
  - hset user address 'beijing'
	

---
## 8.3、应对穿透
**业务系统海量访问压根就不存在的数据，就称为缓存穿透**

**产生原因：**
- 代码逻辑错误
- 恶意攻击/爬虫

**应对策略**
- 缓存"空对象" : 浪费存储空间
- Bloom Filter拦截 : 代码逻辑较复杂(4.0后模块支持)

---
## 8.4、应对雪崩
*缓存雪崩的英文原意是 stampeding herd（奔逃的野牛），指的是缓存层宕掉或者key集中失效后，流量会像奔逃的野牛一样，打向后端存储。*
- 保证缓存服务的高可用(Sentinel/Cluster)
- 限流以及降级
- 缓存重建优化
	- 互斥锁
	- 逻辑过期、异步续期

---

# 9、应用实例
- Strings：token、session、验证码、页面静态化、分布式锁
- Lists：最近联系人
- Sets：用户标签、优惠券（激活码）
- Hashes：购物车
- Sorted Sets：排行榜
- Bitmaps：用户签到、在线状态
- HyperLogLog：日独立总数统计（ip、deviceId）
- Geo：附近的人、摇一摇、两地距离

