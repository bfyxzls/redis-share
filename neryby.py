import redis

conn = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

nearbyKey = 'neryby:'
conn.delete(nearbyKey)

# 模拟加入附近的人
conn.geoadd(nearbyKey, *(116.4162440000, 40.0119070000, 'james'))
conn.geoadd(nearbyKey, *(116.4206630000, 40.0131640000, 'rex'))
conn.geoadd(nearbyKey, *(116.4201420000, 40.0117140000, 'andy'))
conn.geoadd(nearbyKey, *(116.4151660000, 40.0132200000, 'lucy'))
conn.geoadd(nearbyKey, *(116.4162260000, 40.0104150000, 'top'))
#距离较远
conn.geoadd(nearbyKey, *(116.4501280000, 40.0236220000, 'jack'))

# 求james附近1公里范围内的人
print("james 附近一公里范围内的人都有: {}".format(
  conn.georadiusbymember(nearbyKey, 'james', 1, unit='km')))
print("james 和 jack 距离:{}公里".format(
  conn.geodist(nearbyKey, 'james', 'jack', unit='km')))
