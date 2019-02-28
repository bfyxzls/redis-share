import random
import string
import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

dauKey = 'dau:'
conn.flushall()
print("初始时的内存占用是: {} 内存".format(conn.info(section='Memory')['used_memory_human']))


def genc_device():
  code = ''
  for i in range(10):
    code += random.choice(string.ascii_uppercase)
  return code


# 生成10w个 device
deviceArr = []

for i in range(100000):
  deviceArr.append(genc_device())

print("一共生成了 [{}] 个设备请求信息.".format(len(deviceArr)))

conn.sadd(dauKey, *deviceArr)
print("排重后统计结果有 :{}".format(conn.scard(dauKey)))
print("共耗费了 {} 内存".format(conn.info(section='Memory')['used_memory_human']))
conn.flushall()
conn.pfadd(dauKey, *deviceArr)
print("近似统计结果有 :{}".format(conn.pfcount(dauKey)))
print("共耗费了 {} 内存".format(conn.info(section='Memory')['used_memory_human']))
