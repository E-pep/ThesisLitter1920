
import time
import logging

## GUI #######################################################################################################################



import redis

# connect with redis server
redisPublisher = redis.Redis(host="redis", port=6379, db=0)



#start of our main loop --------------------------------------------------------------------------------------------

if __name__ == "__main__":
    while True:
        redisPublisher.publish('mqtt_data', 'testRedis')
        time.sleep(1)