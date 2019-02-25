import random
import string

import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
couponKey = 'coupon:'
conn.delete(couponKey)


def gencCoupon():
  code = ''
  for i in range(6):
    code += random.choice(string.ascii_uppercase)
  return code


for i in range(200):
  code = gencCoupon()
  print("添加code {}, 结果是:{}".format(code, conn.sadd(couponKey, code)))

print("总共优惠码数量是:{}".format(conn.scard(couponKey)))

print("发出一个优惠码:{}, 之后剩余优惠码数量是:{}".format(conn.spop(couponKey), conn.scard(couponKey)))
