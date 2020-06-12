### Authors: mertcanakin, umtaktpe ###

import RPi.GPIO as GPIO
import time
import sys
#import statistics

class Filter:    #Class for sensor values and filters

    # Ultrasonic sensor pins
    TRIG = 23
    ECHO = 24

    def __init__(self):
        GPIO.setmode(GPIO.BCM)      #GPIO Mode
        GPIO.setwarnings(False)  
        
        # Set pin modes
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)   
    
    # Distance calculation function
    def distance_calc(self):
        distances = []

        t_end = time.time() + 60 / 20
        while time.time() < t_end: 
            # set Trigger to HIGH
            GPIO.output(self.TRIG, True)
        
            # set Trigger LOW
            time.sleep(0.0001)
            GPIO.output(self.TRIG, False)
        
            start_time = time.time()
            stop_time = time.time()
        
            # save start time
            while GPIO.input(self.ECHO) == 0:
                start_time = time.time()
        
            # save time of arrival
            while GPIO.input(self.ECHO) == 1:
                stop_time = time.time()
        
            # time difference between start and arrival
            time_diff = stop_time - start_time
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (time_diff * 34300) / 2   

            distances.append('%.2f' % distance)

        return distances
    
    # Kalman Filter function
    def kalman(self, sensor_values):

        var_mea=2.92e-3  #Measurement Noise Covariance
        var_pro=1e-4    #Process Noise Covariance
        P_cov=0.0; KG=0.0; P=1.0; Xp=0.0; Zp=0.0; X_est=0.0
        kalman_values = []

        for i in sensor_values:
            P_cov = P + var_pro              #Predict next covariance
            KG = P_cov/(P_cov + var_mea)     #Compute Kalman Gain
            P = (1-KG)*P_cov                 #Update covariance estimation
            Xp = X_est
            Zp = Xp
            X_est = KG*(float(i)-Zp)+Xp    #Update the state estimation
            kalman_values.append(X_est)
        return kalman_values

    # Low pass filter function
    def low_pass(self, sensor_values):
        alpha=0.5
        data_filtered=[0,0]
        n=1
        lowpass_values = []

        for i in sensor_values:
            data_filtered[n] = alpha * float(i) + (1 - alpha) * data_filtered[n-1]
            data_filtered[n-1] = data_filtered[n]
            lowpass_values.append(data_filtered[n])

        return lowpass_values

    # Average function
    def mean_calc(self, sensor_values):
        array_distance=[0,0]
        j=0
        arr=[]

        for i in sensor_values:
            array_distance.append(float(i))
            mean_values=(array_distance[j]+array_distance[j+1])/2
            arr.append(mean_values)
            j += 1
        return arr

# Opening files for each filter
f_sensor=open('/home/pi/Desktop/log/sensor.txt','a')
f_kalman=open('/home/pi/Desktop/log/kalman.txt','a')
f_mean=open('/home/pi/Desktop/log/mean.txt','a')
f_lowpass=open('/home/pi/Desktop/log/lowpass.txt','a')

sensor = Filter()

#Writing values to files
sensor_values = sensor.distance_calc()
for i in sensor_values:
    f_sensor.write(str(i)+'\n')
f_sensor.flush()


kalman_values=sensor.kalman(sensor_values)
for i in kalman_values:
    f_kalman.write(str(i)+'\n')
f_kalman.flush()


mean_values=sensor.mean_calc(sensor_values)
for i in mean_values:
    f_mean.write(str(i)+'\n')
f_mean.flush()


lowpass_values=sensor.low_pass(sensor_values)
for i in lowpass_values:
    f_lowpass.write(str(i)+'\n')
f_lowpass.flush()



