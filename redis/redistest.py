import redis

r = redis.StrictRedis(host = 'localhost', port=6379, charset="utf-8", decode_responses=True) 

r.set('A', 'candidato1')
r.set('B', 'candidato2')

print(r.get('A'))
