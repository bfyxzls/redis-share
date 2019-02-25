import random
import threading
import time

import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rankingKey = 'rank:key'
conn.delete(rankingKey)


# 模拟消费行为
def consume():
  # 模拟用户id
  user = 'user:{}'.format(random.randint(100, 200))
  # 模拟消费金额
  money = random.randint(100, 10000)
  conn.zincrby(rankingKey, money, user)


for i in range(400):
  threading.Thread(target=consume()).start()
time.sleep(.5)

for m in conn.zrevrange(rankingKey, 0, 9, withscores=True):
  print(m)
