import time
import pwmio
import board


class Servo:
    def __init__(self, pin, pulse_rate=50):
        self.pwm = pwmio.PWMOut(board.GP0, duty_cycle=0, frequency=pulse_rate)
        self.pin = pin
        self.pulse_rate = pulse_rate
        self.angle = None

    def write(self, angle):
        if angle is None:
            pulse_width = 0.0
        else:
            pulse_width = 0.001 + angle * (0.001 / 180.0)
        cycle_period = 1.0 / self.pulse_rate
        duty_cycle = pulse_width / cycle_period
        duty_fixed = int(2 ** 16 * duty_cycle)
        self.pwm.duty_cycle = min(max(duty_fixed, 0), 65535)
        self.angle = angle


def dance_for_time(servo, freq, duration_time,target_angle,steps=50):
    step_time = duration_time / steps
    step_size = (target_angle - servo.angle) / steps
    angle = servo.angle
    for i in range(steps):
        angle += step_size
        servo.write(angle)
        print(step_time)
        time.sleep(step_time)
    return target_angle


def read_csv(file):
    servo = Servo(board.GP0)
    servo.write(90)
    with open(file) as f:
        lines = f.readlines()
    lines = lines[1:]
    start_time = time.time()
    direction = 1  # 1 for up, -1 for down
    swing = 30  # degrees
    for line in lines:
        attrs = line.split(",")
        start_note, duration_time, freq = map(float, attrs)
        while (time.time() - start_time) < start_note:
            continue
        if direction > 0:
            target_angle = 90 + swing
        else:
            target_angle = 90 - swing
        target_angle = dance_for_time(servo, freq,duration_time,target_angle,50)
        direction *= -1


read_csv("notes.csv")
