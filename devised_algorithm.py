#아두이노에서 센서값 체크해서 stable구간에 모두 포함이면 안보내고 하나라도 넘어가면 
#클라우드로 센서 데이터를 보내는거로

#power
power = int(input("Enter Power Available: "))

#soil moisture value array
print("Enter the moisture value: ")
moisture_value = list(map(int, input().split()))

#required power for irrigation 50inch 100inch 200inch 400inch
power_consumption = [[1, 2, 3],[2, 3, 4], [3, 4, 5], [5, 6, 7]]

#calculate level
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

#print("level: ", calculate_level(moisture_value))

level = calculate_level(moisture_value)

def irrigate(power, level):
  final_level = [0, 0, 0, 0]

  #predict power consumption
  expected_power = []
  for i in range(len(level)):
    if level[i] != 0:
      expected_power.append(power_consumption[i][level[i]-1])
    else: 
      expected_power.append(0)

  #print("expected power: ", expected_power)

  #calculate power consumption
  total_power = 0
  for p in expected_power:
    total_power = total_power + p

  #print(total_power)

  #1. power sufficient
  if total_power < power:
    #print(level)
    power = power - total_power #power remain update
    final_level = level
    return final_level

  else: #2. power not sufficient
    #check the power for each
    for i in range(len(expected_power)):
      if power < expected_power[i]:
        level[i] = 0
        expected_power[i] = 0
    
    if sum(level) == 0:
      return [-1]
    
    index = [0, 1, 2, 3]
    while power > 0:
      indices = [index for index, value in enumerate(level) if value == max(level)]
      #print("indices: ", indices)
      for i in indices:
        if power >= expected_power[i]:
          power = power - expected_power[i]
          final_level[i] = level[i]
          level[i] = 0
          #print("power: ", power)
        else:
          power = 0  
      # remain = list(set(index) - set(indices))
      # print("remain: ", remain)
    return final_level
  
print(irrigate(power, level))




