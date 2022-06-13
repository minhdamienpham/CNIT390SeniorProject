import time
import serial
import pymysql

def main():
    #ser = serial.Serial("/dev/ttyACM1", baudrate=9600, timeout=None)
    arduino = serial.Serial("/dev/ttyACM1", baudrate=9600, timeout=None)
    
    Host = "localhost"
    User = "root"
    Password = "0000"
    database = "experiment"
    conn = pymysql.connect(host=Host, user=User, password=Password, database=database)
    
    while True:
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        
        #if ser.in_waiting > 0:
        if arduino.in_waiting > 0:
            #line = ser.readline().decode('utf-8').rstrip()
            line = arduino.readline().decode('utf-8').rstrip()
            
            # print("\n/* Receive Data */")
            # print(line)
            arr = line.split()
            #print(len(arr))
            if len(arr) == 5:
                #print("/* Parsing Data*/")
                print("relay : area:" + str(arr[0]) + ", amount:" + str(arr[1]) + ", level:" + str(arr[2]) + ", remained:" + str(arr[3]) + ", sensor_value: " + str(arr[4])) 
                #time.sleep(0.01)
                cur = conn.cursor()
                query = f"INSERT INTO ex4 (irrigation_time, area, amount_battery, level, remained_battery) VALUES ('"+ current+ "','" + str(arr[0]) + "','" + str(arr[1]) + "','" + str(arr[2]) + "','" + str(arr[3]) +"');"
                cur.execute(query)
                conn.commit()
                
            elif len(arr) == 2:
                print("DB : area:" + str(arr[0]) + ", value:" + str(arr[1]))
                cur = conn.cursor()
                query = f"INSERT INTO ex8 (irrigation_time, area, value) VALUES ('"+ current+ "','" + str(arr[0]) + "','" + str(arr[1]) +"');"
                cur.execute(query)
                conn.commit()

    conn.close()


if __name__ == "__main__":
    main()

