import random
import string
import redis

//定义redis
conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

//定义变量
couponKey = 'coupon:'

conn.delete(couponKey)

//定义方法
def gencCoupon():
  code = ''
  for i in range(6):
    code += random.choice(string.ascii_uppercase)
  return code

//循环
for i in range(200):
  code = gencCoupon()
  print("添加code {}, 结果是:{}".format(code, conn.sadd(couponKey, code)))

//打印
print("总共优惠码数量是:{}".format(conn.scard(couponKey)))

print("发出一个优惠码:{}, 之后剩余优惠码数量是:{}".format(conn.spop(couponKey), conn.scard(couponKey)))
