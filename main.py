from machine import Pin
import time

class TCRT5000:
    def __init__(self, pin):
        self.sensor = Pin(pin, Pin.IN)

    def value(self):
        return self.sensor.value()

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def distance(self):
        self.trigger.off()
        time.sleep_us(2)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        while self.echo.value() == 0:
            pass
        start = time.ticks_us()
        while self.echo.value() == 1:
            pass
        stop = time.ticks_us()
        return (stop - start) / 58

class LN298N:
    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.in3 = Pin(in3_pin, Pin.OUT)
        self.in4 = Pin(in4_pin, Pin.OUT)

    def forward(self):
        self.in1.off()
        self.in2.on()
        self.in3.off()
        self.in4.on()

    def turn_left(self):
        self.in1.off()
        self.in2.off()
        self.in3.off()
        self.in4.on()

    def turn_right(self):
        self.in1.off()
        self.in2.on()
        self.in3.off()
        self.in4.off()

    def stop(self):
        self.in1.off()
        self.in2.off()
        self.in3.off()
        self.in4.off()

    def control(self, mode, tcrt1, tcrt2):
        if mode == "line_follow":
            if tcrt1.value() == 1 and tcrt2.value() == 1:
                self.forward()
            elif tcrt1.value() == 1 and tcrt2.value() == 0:
                self.turn_right()
            elif tcrt1.value() == 0 and tcrt2.value() == 1:
                self.turn_left()
            else:
                self.stop()
        elif mode == "stop":
            self.stop()

tcrt1 = TCRT5000(5)
tcrt2 = TCRT5000(6)
hcsr04 = HCSR04(7, 8)
lm298n = LN298N(1, 2, 3, 4)

run_mode = "line_follow"

while True:
    distance = hcsr04.distance()
    print("Tín hiệu:", tcrt1.value(), tcrt2.value())
    print("Khoảng cách: ", distance, "cm")
    if distance < 20:
        run_mode = "stop"
    else:
        run_mode = "line_follow"
    lm298n.control(run_mode, tcrt1, tcrt2)
    time.sleep(0.01)
