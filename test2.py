# -*- coding: utf-8 -*-
import urllib.request, urllib.parse
import json
import time

dataLocation = '/Users/pengyin/data/serv'
prometheuServer = "10.129.97.141:9090"
#prometheuServer = "143.92.64.63:9090"
#prometheuServer = "10.12.77.196:9090"


prometheus_http_api_url_fixpart_head = 'http://' + prometheuServer + '/api/v1/query_range?query='

targetlist = ["10.129.97.77:9100","10.129.97.141:9100",\
              "10.129.103.79:9100","10.129.103.78:9100",\
              "10.129.103.77:9100","10.129.103.76:9100",\
              "10.129.103.75:9100","10.129.103.74:9100",\
              "10.129.103.168:9100","10.129.103.167:9100",\
              "10.129.103.166:9100","10.129.103.165:9100",\
              "10.129.103.164:9100","10.129.103.163:9100",\
              "10.129.103.112:9100","10.129.103.111:9100",\
              "10.129.103.110:9100","10.129.103.109:9100",\
              "10.129.103.108:9100","10.129.103.107:9100",\
              "10.129.97.81:9100","10.129.99.198:9100",\
              "10.129.99.199:9100","10.129.99.200:9100",\
              "10.129.99.231:9100","10.129.99.232:9100",\
              "10.129.97.76:9100","10.129.97.140:9100"]

redislist = ["10.129.97.77:9100","10.129.97.141:9100","10.129.103.79:9100","10.129.103.78:9100","10.129.103.77:9100"]
kafkalist = ["10.129.103.76:9100","10.129.103.75:9100","10.129.103.74:9100","10.129.103.168:9100","10.129.103.167:9100"]
eslist = ["10.129.103.166:9100","10.129.103.165:9100","10.129.103.164:9100","10.129.103.163:9100","10.129.103.112:9100"]


starttime = '2020-04-26 09:00:00'
endtime = '2020-04-26 10:00:00'
starttime_Stamp = int(time.mktime(time.strptime(starttime, \
                                    "%Y-%m-%d %H:%M:%S")))
endtime_Stamp = int(time.mktime(time.strptime(endtime, \
                                    "%Y-%m-%d %H:%M:%S")))
step = '15s'
prometheus_http_api_url_fixpart_tail = '&start=' + str(starttime_Stamp) + '&end=' + str(endtime_Stamp) + '&step=' + step
#print(prometheus_http_api_url_fixpart_head)
#print(prometheus_http_api_url_fixpart_tail)
datatypelist = ['cpu',  'qps', 'memory', 'disk']
#cputypelist = [c1, c2, c3, c4]
#qpstypelist = [qps1, qps2]



# handle headline
# For CPU
cpuHeadList = ['服务器IP' ,'时间戳' , '本地时间' ,  'CPU使用率%' ,  'CPU内核过去十分钟每秒平均占用时间' , 'CPUIOwait过去十分钟每秒平均占用时间' ,  'CPU用户态过去十分钟每秒平均占用时间']
with open(dataLocation + '/cpu', 'a') as f:
    listToStr = ' ,'.join([str(elem) for elem in cpuHeadList])
    f.write(listToStr + '\n')

# For Network
networkHeadList = ['服务器IP' ,'时间戳' , '本地时间' , '每秒接受到数据字节数' , '每秒发送的数据字节数']
with open(dataLocation + '/qps', 'a') as f:
    listToStr = ' ,'.join([str(elem) for elem in networkHeadList])
    f.write(listToStr + '\n')

# For Memory
memoryHeadList = ['服务器IP' ,'时间戳' , '本地时间' , '内存使用率' , '内存剩余空间MB']
with open(dataLocation + '/memory', 'a') as f:
    listToStr = ' ,'.join([str(elem) for elem in memoryHeadList])
    f.write(listToStr + '\n')

# For Disk
diskHeadList = ['服务器IP' ,'时间戳' , '本地时间' , '磁盘使用率' , '磁盘每秒I/O(MB)']
with open(dataLocation + '/disk', 'a') as f:
    listToStr = ' ,'.join([str(elem) for elem in diskHeadList])
    f.write(listToStr + '\n')

# For report
with open(dataLocation + '/cpureport', 'a') as f:
    line = ["服务器IP" , "CPU最高使用率时间点", "CPU使用率峰值", "CPU I/O wait 峰值时间点", "CPU I/O wait 峰值"]
    listToStr = ' ,'.join([str(elem) for elem in line])
    print(listToStr)
    f.write(listToStr + '\n')



with open(dataLocation + '/qpsreport', 'a') as f:
    line = ['服务器IP' ,'网络receive峰值时间点', '网络receive峰值' , '网络sent 峰值时间点' ,'网络sent 峰值']
    listToStr = ' ,'.join([str(elem) for elem in line])
    f.write(listToStr + '\n')

with open(dataLocation + '/memoryreport', 'a') as f:
    line = ['服务器IP' ,'内存使用率峰值时间点', '内存使用率峰值']
    listToStr = ' ,'.join([str(elem) for elem in line])
    f.write(listToStr + '\n')

with open(dataLocation + '/diskreport', 'a') as f:
    line = ['服务器IP' ,'磁盘使用量峰值','磁盘使用量峰值时间点', '磁盘IO峰值' , '磁盘IO峰值时间点']
    listToStr = ' ,'.join([str(elem) for elem in line])
    f.write(listToStr + '\n')


# Handle MW

with open(dataLocation + '/Middleware', 'a') as f:
    line = ["中间件组件", "ip", "CPU使用率峰值（%）", \
            "网络I/O峰值（bytes）", "内存使用率峰值（%）", \
            "磁盘使用率峰值(%)", "磁盘IO峰值（MB）"]
    listToStr = ' ,'.join([str(elem) for elem in line])
    print(listToStr)
    f.write(listToStr + '\n')

for target in targetlist:

    if target in redislist:
        zujian = "Redis"
    if target in kafkalist:
        zujian = "Kafka"
    if target in eslist:
        zujian = "ES"

    Highest_cpu_usage_value = 0
    Highest_cpu_usage_time = ""
    Highest_cpu_iowait_value = 0
    Highest_cpu_iowait_time = ""

    H_value_n1 = 0
    H_time_n1 = ""
    H_value_n2 = 0
    H_time_n2 = ""

    H_value_m1 = 0
    H_time_m1 = ""
    H_value_m2 = 0
    H_time_m2 = ""


    H_value_d1 = 0
    H_time_d1 = ""
    H_value_d2 = 0
    H_time_d2 = ""


    target = '"' + target + '"'
    instance = 'instance=' + target

    ##########################################################CPU##########################################################

    c_value_list = []

    #target = "10.129.103.75:9100"

    c_value_list.append(target)

    c1 = urllib.parse.quote('1 - (sum(increase(node_cpu_seconds_total{mode="idle",' + instance + '}[1m])) / sum(increase(node_cpu_seconds_total{' + instance + '}[1m])) )')
    c2 = urllib.parse.quote('sum(rate(node_cpu_seconds_total{mode="system",' + instance + '}[1m])) / sum(increase(node_cpu_seconds_total{' + instance + '}[1m]))')
    #print('sum(rate(node_cpu_seconds_total{mode="sys",' + instance + '}[1m]))')
    c3 = urllib.parse.quote('sum(rate(node_cpu_seconds_total{mode="iowait",' + instance + '}[1m])) /  sum(increase(node_cpu_seconds_total{' + instance + '}[1m]))')
    c4 = urllib.parse.quote('sum(rate(node_cpu_seconds_total{mode="user",' + instance + '}[1m])) / sum(increase(node_cpu_seconds_total{' + instance + '}[1m]))')

    c1_url = prometheus_http_api_url_fixpart_head + c1 + prometheus_http_api_url_fixpart_tail
    c2_url = prometheus_http_api_url_fixpart_head + c2 + prometheus_http_api_url_fixpart_tail
    c3_url = prometheus_http_api_url_fixpart_head + c3 + prometheus_http_api_url_fixpart_tail
    c4_url = prometheus_http_api_url_fixpart_head + c4 + prometheus_http_api_url_fixpart_tail

    # get cpu data
    #print(c2_url)
    c1_url_response = urllib.request.urlopen(c1_url)
    c1_url_response_data = c1_url_response.read()
    # convert c1 to dict data tyoe
    c1_dict = json.loads(c1_url_response_data)
    #print(c1_dict['data']['result']['values'][0][1])
    #print(c1_dict['data']['result'])


    #c1_value_list = c1_dict['data']['result'][0]['value'][1]

    c2_url_response = urllib.request.urlopen(c2_url)
    c2_url_response_data = c2_url_response.read()
    # convert c2 to dict data tyoe
    c2_dict = json.loads(c2_url_response_data)
    #print(target, end='c2:')
    #print(c2_dict)

    c3_url_response = urllib.request.urlopen(c3_url)
    c3_url_response_data = c3_url_response.read()
    # convert c3 to dict data type
    c3_dict = json.loads(c3_url_response_data)
    #print(target, end=':')
    #print(c3_dict)

    c4_url_response = urllib.request.urlopen(c4_url)
    c4_url_response_data = c4_url_response.read()
    # convert c4 to dict data tyoe
    c4_dict = json.loads(c4_url_response_data)
    #print(target, end=':')
    #print(c4_dict)
    if not c1_dict['data']['result']:
        continue
    #print(c1_dict)
    #print(c1_dict['data']['result'][0]['values'])
    leng = len(c1_dict['data']['result'][0]['values'])

    if leng <= 0:
        continue
    i = 0
    while i < leng:
        time_Stamp = c1_dict['data']['result'][0]['values'][i][0]
        localtime_tuple = time.localtime(time_Stamp)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime_tuple)
        c_value_list.append(time_Stamp)
        c_value_list.append(localtime)
        if c1_dict['data']['result']:
            if c1_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(c1_dict['data']['result'][0]['values'][0][1])
                c1_value = float(c1_dict['data']['result'][0]['values'][i][1])
                c1_value = c1_value * 100
                #print("c1: ", end='')
                #print(c1_value)
                c_value_list.append(c1_value)

                # for cpu report
                if c1_value > Highest_cpu_usage_value :
                    Highest_cpu_usage_value = c1_value
                    Highest_cpu_usage_time = localtime

        if c2_dict['data']['result']:
            if c2_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(c2_dict['data']['result'][0]['values'][0][1])
                c2_value = float(c2_dict['data']['result'][0]['values'][i][1])
                c2_value = c2_value * 100
                #print("c2: ", end='')
                #print(c2_value)
                c_value_list.append(c2_value)

                # for cpu report


        if c3_dict['data']['result']:
            if c3_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(c3_dict['data']['result'][0]['values'][0][1])
                c3_value = float(c3_dict['data']['result'][0]['values'][i][1])
                c3_value = c3_value * 100
                #print("c3: ", end='')
                #print(c3_value)
                c_value_list.append(c3_value)

                # for cpu report
                if c3_value > Highest_cpu_iowait_value:
                    Highest_cpu_iowait_value = c3_value
                    Highest_cpu_iowait_time = localtime


        if c4_dict['data']['result']:
            if c4_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(c4_dict['data']['result'][0]['values'][0][1])
                c4_value = float(c3_dict['data']['result'][0]['values'][i][1])
                c4_value = c4_value * 100
                c_value_list.append(c4_value)
                #print("c4: ", end='')
                #print(c4_value)

                # for cpu report



        with open(dataLocation + '/cpu', 'a') as f:
            listToStr = ' ,'.join([str(elem) for elem in c_value_list])
            f.write(listToStr + '\n')
        #print(c_value_list)
        c_value_list = []
        c_value_list.append(target)
        i = i + 1

    ########handle report by instance
    with open(dataLocation + '/cpureport', 'a') as f:
        line = [target, Highest_cpu_usage_time, Highest_cpu_usage_value, Highest_cpu_iowait_time, Highest_cpu_iowait_value]
        listToStr = ' ,'.join([str(elem) for elem in line])
        #print(listToStr)
        f.write(listToStr + '\n')




##########################################################CPU##########################################################






##########################################################Network######################################################

    n_value_list = []


    n_value_list.append(target)

    n1 = urllib.parse.quote('sum(rate(node_network_receive_bytes_total{' + instance + '}' + '[1m]))')
    n2 = urllib.parse.quote('sum(rate(node_network_transmit_bytes_total{' + instance + '}' + '[1m]))')

    n1_url = prometheus_http_api_url_fixpart_head + n1 + prometheus_http_api_url_fixpart_tail
    n2_url = prometheus_http_api_url_fixpart_head + n2 + prometheus_http_api_url_fixpart_tail

    #print("instance", instance)
    #print("n1", n1)
    #print(prometheus_http_api_url_fixpart_head)
    #print("n1_url", n1_url)


    n1_url_response = urllib.request.urlopen(n1_url)
    n1_url_response_data = n1_url_response.read()

    n1_dict = json.loads(n1_url_response_data)

    #print("n1data:", n1_dict)

    n2_url_response = urllib.request.urlopen(n2_url)
    n2_url_response_data = n2_url_response.read()

    n2_dict = json.loads(n2_url_response_data)

    #print("n1data:", n2_dict)
    if not n1_dict['data']['result']:
        continue

    leng = len(n1_dict['data']['result'][0]['values'])

    if leng <= 0:
        continue
    i = 0
    while i < leng:
        time_Stamp = n1_dict['data']['result'][0]['values'][i][0]
        localtime_tuple = time.localtime(time_Stamp)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime_tuple)
        n_value_list.append(time_Stamp)
        n_value_list.append(localtime)
        if n1_dict['data']['result']:
            if n1_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(n1_dict['data']['result'][0]['values'][0][1])
                n1_value = float(n1_dict['data']['result'][0]['values'][i][1])
                # print("c1: ", end='')
                # print(c1_value)
                n_value_list.append(n1_value)

                # for report
                if n1_value > H_value_n1:
                    H_time_n1 = localtime
                    H_value_n1 = n1_value

        if n2_dict['data']['result']:
            if n2_dict['data']['result'][0]['values']:
                # print(target,end=':')
                # print(c2_dict['data']['result'][0]['values'][0][1])
                n2_value = float(n2_dict['data']['result'][0]['values'][i][1])
                # print("c2: ", end='')
                # print(c2_value)
                n_value_list.append(n2_value)

                if n2_value > H_value_n2:
                    H_time_n2 = localtime
                    H_value_n2 = n2_value



        with open(dataLocation + '/qps', 'a') as f:
            listToStr = ' ,'.join([str(elem) for elem in n_value_list])
            f.write(listToStr + '\n')
        #print(n_value_list)
        n_value_list = []
        n_value_list.append(target)
        i = i + 1


    with open(dataLocation + '/qpsreport', 'a') as f:
        line = [target, H_time_n1, H_value_n1, H_time_n2, H_value_n2]
        listToStr = ' ,'.join([str(elem) for elem in line])
        f.write(listToStr +'\n')


##########################################################Network######################################################







##########################################################Memory######################################################

    m_value_list = []

    # target = "10.129.103.75:9100"
    #target = '"' + target + '"'
    instance = 'instance=' + target
    m_value_list.append(target)

    m1 = urllib.parse.quote("(1 - ((node_memory_Buffers_bytes{"   + \
                            instance +   "} + node_memory_Cached_bytes{"   + \
                            instance +  "} + node_memory_MemFree_bytes{"   + \
                            instance +    "}) / node_memory_MemTotal_bytes{"   + \
                            instance +    "})) * 100")

    m2 = urllib.parse.quote('node_memory_MemTotal_bytes{' + instance + '} /1024 /1024' )

    m1_url = prometheus_http_api_url_fixpart_head + m1 + prometheus_http_api_url_fixpart_tail
    m2_url = prometheus_http_api_url_fixpart_head + m2 + prometheus_http_api_url_fixpart_tail
    '''
        print("instance", instance)
        print("n1", n1)
        print(prometheus_http_api_url_fixpart_head)
        print("n1_url", n1_url)
    '''

    m1_url_response = urllib.request.urlopen(m1_url)
    m1_url_response_data = m1_url_response.read()

    m1_dict = json.loads(m1_url_response_data)

    #print("n1data:", n1_dict)

    m2_url_response = urllib.request.urlopen(m2_url)
    m2_url_response_data = m2_url_response.read()

    m2_dict = json.loads(m2_url_response_data)

    #print("n1data:", n2_dict)
    if not m1_dict['data']['result']:
        continue

    leng = len(m1_dict['data']['result'][0]['values'])

    if leng <= 0:
        continue
    i = 0
    while i < leng:
        time_Stamp = m1_dict['data']['result'][0]['values'][i][0]
        localtime_tuple = time.localtime(time_Stamp)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime_tuple)
        m_value_list.append(time_Stamp)
        m_value_list.append(localtime)
        if m1_dict['data']['result']:
            if m1_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(n1_dict['data']['result'][0]['values'][0][1])
                m1_value = float(m1_dict['data']['result'][0]['values'][i][1])
                # print("c1: ", end='')
                # print(c1_value)
                m_value_list.append(m1_value)

                # for report
                if m1_value > H_value_m1:
                    H_value_m1 = m1_value
                    H_time_m1 = localtime

        if m2_dict['data']['result']:
            if m2_dict['data']['result'][0]['values']:
                # print(target,end=':')
                # print(c2_dict['data']['result'][0]['values'][0][1])
                m2_value = float(m2_dict['data']['result'][0]['values'][i][1])
                # print("c2: ", end='')
                # print(c2_value)
                m_value_list.append(m2_value)

                # for report

                if m2_value > H_value_m2:
                    H_value_m2 = m2_value
                    H_time_m2 = localtime




        with open(dataLocation + '/memory', 'a') as f:
            listToStr = ' ,'.join([str(elem) for elem in m_value_list])
            f.write(listToStr + '\n')
        #print(m_value_list)
        m_value_list = []
        m_value_list.append(target)
        i = i + 1

    # for report
    with open(dataLocation + '/memoryreport', 'a') as f:
        line = [target, H_time_m1, H_value_m1]
        listToStr = ' ,'.join([str(elem) for elem in line])
        f.write(listToStr + '\n')

    ##########################################################Memory######################################################





##########################################################Disk######################################################

    d_value_list = []


    d_value_list.append(target)

    #磁盘使用比例
    d1 = urllib.parse.quote('1 - sum(node_filesystem_free_bytes{' \
                            + instance + '}) / sum(node_filesystem_size_bytes{'  \
                            + instance + '})')
    '''
    print('sum(node_filesystem_free_bytes{' \
                            + instance + '}) / sum(node_filesystem_size_bytes{'  \
                            + instance + '})')
    '''
    #磁盘每秒I/O， MB
    d2 = urllib.parse.quote('sum(rate(node_disk_read_bytes_total{' \
                            + instance +         '}[1m])) + sum(rate(node_disk_written_bytes_total{' \
                            + instance +          '}[1m])) /1024 /1024')
    #print('rate(node_disk_read_bytes_total[1m]){'     + instance +         '} + rate(node_disk_read_bytes_total'  + instance +          '}[1m]) /1024 /1024')
    d1_url = prometheus_http_api_url_fixpart_head + d1 + prometheus_http_api_url_fixpart_tail
    d2_url = prometheus_http_api_url_fixpart_head + d2 + prometheus_http_api_url_fixpart_tail

    #print("instance", instance)
    #print("n1", n1)
    #print(prometheus_http_api_url_fixpart_head)
    #print("n1_url", n1_url)


    d1_url_response = urllib.request.urlopen(d1_url)
    d1_url_response_data = d1_url_response.read()

    d1_dict = json.loads(d1_url_response_data)

    #print("n1data:", n1_dict)

    d2_url_response = urllib.request.urlopen(d2_url)
    d2_url_response_data = d2_url_response.read()

    d2_dict = json.loads(d2_url_response_data)

    #print("n1data:", n2_dict)
    if not d1_dict['data']['result']:
        continue

    leng = len(d1_dict['data']['result'][0]['values'])

    if leng <= 0:
        continue
    i = 0
    while i < leng:
        time_Stamp = d1_dict['data']['result'][0]['values'][i][0]
        localtime_tuple = time.localtime(time_Stamp)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime_tuple)
        d_value_list.append(time_Stamp)
        d_value_list.append(localtime)
        if d1_dict['data']['result']:
            if d1_dict['data']['result'][0]['values']:
                #print(target,end=':')
                #print(n1_dict['data']['result'][0]['values'][0][1])
                #print()
                d1_value = float(d1_dict['data']['result'][0]['values'][i][1])
                #print(d1_value)
                # print("c1: ", end='')
                # print(c1_value)
                d_value_list.append(d1_value)

                # for report

                if d1_value > H_value_d1:
                    H_value_d1 = d1_value
                    H_time_d1 = localtime

        if d2_dict['data']['result']:
            if d2_dict['data']['result'][0]['values']:
                # print(target,end=':')
                # print(c2_dict['data']['result'][0]['values'][0][1])
                d2_value = float(d2_dict['data']['result'][0]['values'][i][1])
                # print("c2: ", end='')
                # print(c2_value)
                d_value_list.append(d2_value)

                if d2_value > H_value_d2:
                    H_value_d2 = d2_value
                    H_time_d2 = localtime


        with open(dataLocation + '/disk', 'a') as f:
            listToStr = ' ,'.join([str(elem) for elem in d_value_list])
            f.write(listToStr + '\n')
        #print(d_value_list)
        d_value_list = []
        d_value_list.append(target)
        i = i + 1

    with open(dataLocation + '/diskreport', 'a') as f:
        line = [target, H_value_d1, H_time_d1, H_value_d2, H_time_d2]
        listToStr = ' ,'.join([str(elem) for elem in line])
        f.write(listToStr + '\n')


    with open(dataLocation + '/Middleware', 'a') as f:
        ip = ""
        ip = target.split(":")[0]
        line = [zujian, ip + '"', Highest_cpu_usage_value, \
                H_value_n1 + H_value_n2, H_value_m1, \
                H_value_d1, H_value_d2]
        listToStr = ' ,'.join([str(elem) for elem in line])
        print(listToStr)
        f.write(listToStr + '\n')

##########################################################Disk######################################################
