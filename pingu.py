#!/usr/local/bin/python3
import re

dataLocation = '/home/pengyin'
filename = dataLocation + "/Middleware"
filename_for_write = dataLocation + "/pinggu"

Redis_threadhold = 0.8
Kafka_threadhold = 0.9
ES_threadhold = 0.7
resourcestims = 10


# 计算所需资源个数
def get_needed_resources(current_resouce_count_by_instance, resoure_threadhold, avgHigestresourcevalue, resourcetimes):
    needed_resources_count = resourcetimes - ((resoure_threadhold - avgHigestresourcevalue) / avgHigestresourcevalue)
    return needed_resources_count

# test1 = 10 - ((0.8 - 0.2) / 0.2)


Redislist = []
Redislist.append("Redis")
Redislist_IP = []
Redislist_c = []
Redislist_n = []
Redislist_m = []
Redislist_d1 = []
Redislist_d2 = []

Kafkalist = []
Kafkalist.append("Kafka")
Kafkalist_IP = []
Kafkalist_c = []
Kafkalist_n = []
Kafkalist_m = []
Kafkalist_d1 = []
Kafkalist_d2 = []

ESlist = []
ESlist.append("ES")
ESlist_IP = []
ESlist_c = []
ESlist_n = []
ESlist_m = []
ESlist_d1 = []
ESlist_d2 = []


# get resourcecount and resoucelist
with open(filename, "r") as f:
    next(f)
    r_count = 0
    k_count = 0
    e_count = 0
    for line in f:
        if re.search(r'^Redis', line):
            g = re.search(r'^Redis', line)
            #Redislist.append(g.group(0))
            line = line.rstrip("\n")
            l = line.split(",")
            #Redislist_IP.append(l[1])
            Redislist_c.append(float(l[2].strip()))
            Redislist_n.append(float(l[3].strip()))
            Redislist_m.append(float(l[4].strip()))
            Redislist_d1.append(float(l[5].strip()))
            Redislist_d2.append(float(l[6].strip()))
            r_count += 1
        elif re.search(r'^Kafka', line):
            g = re.search(r'^Kafka', line)
            #Kafkalist.append(g.group(0))
            line = line.rstrip("\n")
            l = line.split(",")
            #Kafkalist_IP.append(l[1])
            Kafkalist_c.append(float(l[2].strip()))
            Kafkalist_n.append(float(l[3].strip()))
            Kafkalist_m.append(float(l[4].strip()))
            Kafkalist_d1.append(float(l[5].strip()))
            Kafkalist_d2.append(float(l[6].strip()))
            k_count = k_count + 1
        elif re.search(r'^ES', line):
            g = re.search(r'^ES', line)
            #ESlist.append(g.group(0))
            l = line.split(",")
            #ESlist_IP.append(l[1])
            ESlist_c.append(float(l[2].strip()))
            ESlist_n.append(float(l[3].strip()))
            ESlist_m.append(float(l[4].strip()))
            ESlist_d1.append(float(l[5].strip()))
            ESlist_d2.append(float(l[6].strip()))
            e_count = e_count + 1

        else:
            pass


"""
print(Redislist)
print(Redislist_IP)
print(Redislist_c)
print(Redislist_n)
print(Redislist_m)
print(Redislist_d1)
print(Redislist_d2)
"""

#listToStr = ""
#print(Redislist_IP)
#listToStr = ' ，'.join([str(elem) for elem in Redislist_IP])
#print(listToStr)
#r_tpye = "Redis"

avg_redis_c = sum(Redislist_c) / len(Redislist_c)


avg_redis_n = sum(Redislist_n) / len(Redislist_n)

avg_redis_m = sum(Redislist_m) / len(Redislist_m)
#print(avg_redis_m)
avg_redis_d1 = sum(Redislist_d1) / len(Redislist_d1)

avg_redis_d2 = sum(Redislist_d2) / len(Redislist_d2)
#print(avg_redis_d2)
#Redislist.append(listToStr)


Redislist.append(avg_redis_n)
Redislist.append(avg_redis_m)
Redislist.append(avg_redis_d1)
Redislist.append(avg_redis_d2)

Redislist.append(avg_redis_c)
Redislist.append(r_count)   # 当前的redis实例数

# 需要的cpu倍数
redis_c = get_needed_resources(r_count, Redis_threadhold, avg_redis_c/100, resourcestims)
if redis_c <= 0:
    redis_c = 0

Redislist.append(resourcestims)
Redislist.append(redis_c)  # 实际需要添加的倍数
#print(Redislist)





# For Kafka

avg_kafka_c = sum(Kafkalist_c) / len(Kafkalist_c)

avg_kafka_n = sum(Kafkalist_n) / len(Kafkalist_n)

avg_kafka_m = sum(Kafkalist_m) / len(Kafkalist_m)

avg_kafka_d1 = sum(Kafkalist_d1) / len(Kafkalist_d1)

avg_kafka_d2 = sum(Kafkalist_d2) / len(Kafkalist_d2)


Kafkalist.append(avg_kafka_n)
Kafkalist.append(avg_kafka_m)
#print(avg_redis_m)
Kafkalist.append(avg_kafka_d1)
Kafkalist.append(avg_kafka_d2)

Kafkalist.append(avg_kafka_c)
Kafkalist.append(r_count)   # 当前的redis实例数

# 需要的cpu倍数
kafka_c = get_needed_resources(k_count, Kafka_threadhold , avg_kafka_c/100, resourcestims)
if kafka_c <= 0:
    kafka_c = 0

Kafkalist.append(resourcestims)
Kafkalist.append(kafka_c)  # 实际需要添加的倍数
#print(Kafkalist)






# For ES

avg_es_c = sum(ESlist_c ) / len(ESlist_c)

avg_es_n = sum(ESlist_n) / len(ESlist_n)

avg_es_m = sum(ESlist_m) / len(ESlist_m)

avg_es_d1 = sum(ESlist_d1) / len(ESlist_d1)

avg_es_d2 = sum(ESlist_d2) / len(ESlist_d2)


ESlist.append(avg_es_n)
ESlist.append(avg_es_m)
ESlist.append(avg_es_d1)
ESlist.append(avg_es_d2)
ESlist.append(avg_es_c)
#print(e_count)
ESlist.append(e_count)   # 当前的redis实例数

# 需要的cpu倍数
ESlist_c = get_needed_resources(e_count, ES_threadhold, avg_es_c/100, resourcestims)
#print(ESlist_c)
if ESlist_c <= 0:
    ESlist_c = 0

ESlist.append(resourcestims)
ESlist.append(ESlist_c)  # 实际需要添加的倍数
#print(ESlist)
#print(e_count)

# write into file

#headline = ["组件名称" ,  "平均内存峰值" , "平均网络峰值" , "平均磁盘使用峰值" , "平均磁盘读写率峰值" , \
#            "平均CPU高峰" ,  " 当前组件个数", "所需扩容倍数" ,"实际需要倍数"]

with open(filename_for_write, 'a') as f:
    headline = ["组件名称", "平均网络峰值", "平均内存峰值", "平均磁盘峰值", "平均磁盘读写率峰值", \
                "平均CPU高峰", " 当前组件个数", "所需扩容倍数", "实际需要倍数"]
    headlinelistToStr = ' ,'.join([str(elem) for elem in headline])
    # print(listToStr)
    f.write(headlinelistToStr + '\n')
    #print(headlinelistToStr)

    R_listToStr = ' ,'.join([str(elem) for elem in Redislist])
    #print(R_listToStr)
    f.write(R_listToStr + '\n')
    print(Redislist)

    K_listToStr = ' ,'.join([str(elem) for elem in Kafkalist])
    #print(K_listToStr)
    f.write(K_listToStr + '\n')
    print(Kafkalist)
    E_listToStr = ' ,'.join([str(elem) for elem in ESlist])
    #print(E_listToStr)
    f.write(E_listToStr + '\n')
    print(ESlist)






