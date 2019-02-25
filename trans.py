import threading
import time

import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
itemKey = 'item:01'
conn.delete(itemKey)
conn.set(itemKey, 2)


def notrans():
  count = int(conn.get(itemKey))
  time.sleep(.1)
  if count > 0:
    conn.set(itemKey, count - 1)
    print('库存大于0,可以消减', threading.currentThread().ident)
  else:
    print('库存光了', threading.currentThread().ident)


def trans():
  with conn.pipeline() as pipeline:
    while 1:
      try:
        pipeline.watch(itemKey)
        count = int(conn.get(itemKey))
        time.sleep(.1)
        if count > 0:
          pipeline.multi()
          pipeline.set(itemKey, count - 1)
          pipeline.execute()
          print('库存大于0,成功消减,抢到了', threading.currentThread().ident)
        else:
          print("库存光了,没抢到", threading.currentThread().ident)

        break
      except Exception:
        print('库存被其它线程改变了,重试...', threading.currentThread().ident)
        continue


for i in range(3):
  threading.Thread(target=trans()).start()
time.sleep(.5)

print("处理完毕后的库存情况是:", conn.get(itemKey))
