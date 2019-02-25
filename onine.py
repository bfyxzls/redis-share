import random

import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

onlineKey = 'uid:'
conn.flushall()

print("初始时的内存占用是: {} 内存".format(conn.info(section='Memory')['used_memory_human']))


#生成20w用户的登录状态
for i in range(20000):
  conn.setbit(onlineKey, random.randint(100, 2000000), random.randint(0, 1))

print("当前在线用户有: {} 个".format(conn.bitcount(onlineKey)))

print("结束时的内存占用是: {} 内存".format(conn.info(section='Memory')['used_memory_human']))

#20w数据 内存占用 1.20M 内存
#千万级数据,内存占用几百兆
