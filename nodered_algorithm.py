## node-red
import base64
import time

print("msg: ", msg)
newMsg = msg['payload']
decoded_value = newMsg.encode('utf-8')
print("decoded: ", decoded_value)
print(type(decoded_value))

#아두이노에서 센서값 체크해서 stable구간에 모두 포함이면 안보내고 하나라도 넘어가면 
#클라우드로 센서 데이터를 보내는거로

f = open("/home/pi/Desktop/prepower.txt", 'r')
pre_power = f.readlines()
print("file power: ", pre_power)
print(type(pre_power))
f.close()

power2 = int(pre_power[0])
print("power2 type : ", type(power2))
print("power2: ", power2)

'''variable for DB'''
power = power2
#power = int(power)

amount_battery = [0, 0, 0, 0]  # db에 넣을 각각 배터리 소모량
remained_battery = [0, 0, 0, 0]  # 각 relay가 실행될 때, 남은 배터리양 => 각각 그때의 power 변수로 선언함
db_level = []  # 요청한 level

# required power for irrigation 50inch 100inch 200inch 400inch
power_consumption = [[1, 2, 3],[2, 3, 4], [3, 4, 5], [5, 6, 7]]


# soil moisture value 가져오기 => [355, 200, 130, 200]
# soil moisture value array
# print("Enter the moisture value: ")
# moisture_value = list(map(int, input().split()))
string_list = list(decoded_value.split())
print("string_list: ", string_list)
string_list.pop(4)
moisture_value = map(int, string_list)
print('moisture_value: ', type(moisture_value[0]))

# calculate level
def calculate_level(moisture_value):
  level = []
  for value in moisture_value:
    if value > 395:
      level.append(3)
    elif value > 370:
      level.append(2)
    elif value > 355:
      level.append(1)
    else:
      level.append(0)
  return level

# level 계산 => [2, 3, 0, 1]
# print("level: ", calculate_level(moisture_value))
level = calculate_level(moisture_value)

# 실제 relay level 계산
def irrigate(power, level, amount_battery, remained_battery):
  final_level = [0, 0, 0, 0]
  # print("level: ", level)

  # predict power consumption
  expected_power = []
  for i in range(len(level)):
    if level[i] != 0:
      expected_power.append(power_consumption[i][level[i]-1])
    else: 
      expected_power.append(0)

  # print("expected power: ", expected_power)

  # calculate power consumption
  total_power = 0
  for p in expected_power:
    total_power = total_power + p

  #print(total_power)

  #1. power sufficient
  if total_power < power:
    tmp_power = power
    power = power - total_power #power remain update
    final_level = level
    amount_battery = expected_power ## for DB
    for j in range(4):
      remained_battery[j] = tmp_power - expected_power[j]
      tmp_power = remained_battery[j]
    print("expected: ", expected_power)
    print("amount_battery: ", amount_battery)
    print("remained_battery: ", remained_battery)
    return final_level, amount_battery, remained_battery

  else: #2. power not sufficient
    #check the power for each
    for i in range(len(expected_power)):
      if power < expected_power[i]:
        level[i] = 0
        expected_power[i] = 0
        amount_battery[i] = 0  # DB
    
    if sum(level) == 0:
      return [-1]
      
    index = [0, 1, 2, 3]
    while power > 0:
      indices = [index for index, value in enumerate(level) if value == max(level)]
      #print("indices: ", indices)

      for i in indices:
        print("<<test start>>")
        if power >= expected_power[i]:
          print("power: ", type(power))
          print("expected_power: ", type(expected_power[i]))
          print("remained_battery: ", type(remained_battery[i]))
          print("final_level: ", type(final_level[i]))
          print("level: ", type(level[i]))
          
          amount_battery[i] = expected_power[i]
          power = power - expected_power[i]
          remained_battery[i] = power  # DB
          final_level[i] = level[i]
          level[i] = 0
          #print("power: ", power)
        else:
          power = 0  
      print("test7")
      #remain = list(set(index) - set(indices))
      print("test8")
      #print("remain: ", remain)
    
    # print("final_level: ", final_level)
    # print("amount_battery: ", amount_battery)
    # print("remained_battert: ", remained_battery)
    print("test9")
    return final_level, amount_battery, remained_battery
  
irrigation, amount_battery, remained_battery = irrigate(power, level, amount_battery, remained_battery)
print(irrigation)
db_level = irrigation  ## DB

irrigation_command = "".join(map(str, irrigation))

print(irrigation_command)
print("test5555")


# message_byte = myMsg.encode('ascii')
# base64_bytes = base64.b64encode(message_byte)
# base64_message = base64_bytes.decode('ascii')

# Database(MariaDB)
irrigation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
tmp_msg = ""

print("test5555")


for i in range(4):
    #if level[i] != 0:
    tmp_msg = tmp_msg + "INSERT INTO ex3 (irrigation_time, area, amount_battery, level, remained_battery) VALUES ('" + irrigation_time + "','" + str(i) + "','" + str(amount_battery[i]) + "','" + str(db_level[i]) + "','" + str(remained_battery[i]) +"');"
    print(tmp_msg)
        
    f2 = open("/home/pi/Desktop/prepower.txt", 'w')
    data = str(remained_battery[3])
    f2.write(data)
    f2.close()
    print("write: ", data)
        
msg['topic'] = tmp_msg
msg['payload'] = irrigation_command




return msg