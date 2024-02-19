from flask import Flask, render_template, request
from adafruit_servokit import ServoKit
import atexit
# for motors
import RPi.GPIO as gpio
import time
from RpiMotorLib import rpi_dc_lib

app = Flask(__name__)

# Set up PCA9685 and initialize servos
kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(500, 2500)
kit.servo[3].set_pulse_width_range(500, 2500)
kit.servo[4].set_pulse_width_range(500, 2500)
kit.servo[5].set_pulse_width_range(500, 2500)
kit.servo[8].set_pulse_width_range(500, 2500)
kit.servo[9].set_pulse_width_range(500, 2500)

# Define servo positions for channel 1
servo1_pos = 90  # Initial position
servo2_pos = 90

# Define servo positions for channel 2
servo3_pos = 90  # Initial position
servo4_pos = 90

# Define servo positions for channel 3
servo5_pos = 90  # Initial position
servo6_pos = 90

# Define servo positions for channel 4
servo7_pos = 90  # Initial position
servo8_pos = 90

# Cleanup function to stop servos on exit
def cleanup():
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90
    kit.servo[3].angle = 90
    kit.servo[4].angle = 90
    kit.servo[5].angle = 90
    kit.servo[8].angle = 90
    kit.servo[9].angle = 90

atexit.register(cleanup)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move_servo', methods=['POST'])
def move_servo():
    global servo1_pos, servo2_pos

    direction = request.form['direction']
    step = int(request.form['step'])

    if direction == 'left':
        servo1_pos += step
    elif direction == 'right':
        servo1_pos -= step
    elif direction == 'up':
        servo2_pos += step
    elif direction == 'down':
        servo2_pos -= step

    servo1_pos = max(0, min(180, servo1_pos))
    servo2_pos = max(0, min(180, servo2_pos))

    kit.servo[0].angle = servo1_pos
    kit.servo[1].angle = servo2_pos

    return 'OK'

@app.route('/move_servo_channel2', methods=['POST'])
def move_servo_channel2():
    global servo3_pos, servo4_pos

    direction = request.form['direction']
    step = int(request.form['step'])

    if direction == 'left':
        servo3_pos += step
    elif direction == 'right':
        servo3_pos -= step

    servo3_pos = max(0, min(180, servo3_pos))

    kit.servo[2].angle = servo3_pos

    return 'OK'

@app.route('/move_servo_channel3', methods=['POST'])
def move_servo_channel3():
    global servo4_pos, servo5_pos

    direction = request.form['direction']
    step = int(request.form['step'])

    if direction == 'up':
        servo4_pos += step
    elif direction == 'down':
        servo4_pos -= step

    servo4_pos = max(0, min(180, servo4_pos))

    kit.servo[3].angle = servo4_pos

    return 'OK'

@app.route('/move_servo_channel4', methods=['POST'])
def move_servo_channel4():
    global servo5_pos, servo6_pos

    direction = request.form['direction']
    step = int(request.form['step'])

    if direction == 'up':
        servo5_pos += step
    elif direction == 'down':
        servo5_pos -= step

    servo5_pos = max(0, min(180, servo5_pos))

    kit.servo[4].angle = servo5_pos

    return 'OK'

@app.route('/move_servo_channel8_and_9', methods=['POST'])
def move_servo_channel8_and_9():
    global servo7_pos, servo8_pos

    direction = request.form['direction']
    step = int(request.form['step'])

    if direction == 'left':
        servo7_pos += step
    elif direction == 'right':
        servo7_pos -= step
    elif direction == 'up':
        servo8_pos += step
    elif direction == 'down':
        servo8_pos -= step

    servo7_pos = max(0, min(180, servo7_pos))
    servo8_pos = max(0, min(180, servo8_pos))

    kit.servo[8].angle = servo7_pos
    kit.servo[9].angle = servo8_pos

    return 'OK'

@app.route('/set_midway', methods=['POST'])
def set_midway():
    kit.servo[2].angle = 90
#    kit.servo[8].angle = 90
    return 'OK'

# motor control via l298n
def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(13, gpio.OUT)

def forward_slow(sec):
    init()
    pwm17 = gpio.PWM(12,100)
    pwm22 = gpio.PWM(13,100)
    t=40
    pwm17.start(t)
    pwm22.start(t)

    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)

    time.sleep(sec)
    pwm17.stop(t)
    pwm22.stop(t)
    gpio.cleanup()

def forward_faster(sec):
    init()
    pwm17 = gpio.PWM(12,100)
    pwm22 = gpio.PWM(13,100)
    t=75
    pwm17.start(t)
    pwm22.start(t)

    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)

    time.sleep(sec)
    pwm17.stop(t)
    pwm22.stop(t)
    gpio.cleanup()

def forward_fastest(sec):
    init()
    pwm17 = gpio.PWM(12,100)
    pwm22 = gpio.PWM(13,100)
    t=100
    pwm17.start(t)
    pwm22.start(t)

    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)

    time.sleep(sec)
    pwm17.stop(t)
    pwm22.stop(t)
    gpio.cleanup()

def reverse(sec):
    init()
    pwm17 = gpio.PWM(12,100)
    pwm22 = gpio.PWM(13,100)
    t=100
    pwm17.start(t)
    pwm22.start(t)

    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()

def reverse_slow(sec):
    init()
    # Initialize PWM objects
    pwm17 = gpio.PWM(12, 100)
    pwm22 = gpio.PWM(13, 100)

    # Start PWM
    t = 100
    pwm17.start(t)
    pwm22.start(t)

    # Reverse motor direction
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)

    # Sleep for the specified duration
    time.sleep(sec)

# Stop PWM
    pwm17.stop()
    pwm22.stop()

# Cleanup GPIO
    gpio.cleanup()

@app.route('/move_forward', methods=['POST'])
def forward():
    forward(1)  # You can adjust the time as needed
    return 'Forwarding...'

# Initialize GPIO only once
init_done = False

@app.route('/forward_slow', methods=['POST'])
def forward_slow():
    global init_done
    # Ensure GPIO initialization is done only once
    if not init_done:
      init()
      init_done = True
    # Extract 'direction' from the request data
    direction = request.json.get('direction')
    # Handle the motor control based on the direction
    if direction == 'up':
        # Your motor control code for forward motion
#        pass  # Replace 'pass' with your actual motor control code
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        gpio.setup(12, gpio.OUT)
        gpio.setup(13, gpio.OUT)
#        pwm17 = gpio.PWM(12,100)
#        pwm22 = gpio.PWM(13,100)
        gpio.output(17, False)
        gpio.output(22, True)
        gpio.output(23, True)
        gpio.output(24, False)
    # Return a response
    return 'Forwarding...'

@app.route('/stop', methods=['POST'])
def stop():
    gpio.cleanup()
    return 'Stopped'

@app.route('/reverse', methods=['POST'])
def reverse():
    reverse_slow(5)  # You can adjust the time as needed
    return 'Reverse ...'

@app.route('/move_reverse', methods=['POST'])
def move_reverse():
    global init_done
    # Ensure GPIO initialization is done only once
    if not init_done:
      init()
      init_done = True
    # Extract 'direction' from the request data
    direction = request.json.get('direction')
    # Handle the motor control based on the direction
    if direction == 'down':
        # Your motor control code for reverse motion
#        pass  # Replace 'pass' with your actual motor control code
        gpio.setmode(gpio.BCM)
        gpio.setup(17, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        gpio.setup(12, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        pwm17 = gpio.PWM(12,100)
        pwm22 = gpio.PWM(13,100)
        gpio.output(17, True)
        gpio.output(22, False)
        gpio.output(23, False)
        gpio.output(24, True)
    # Return a response
    return 'Backing Up ...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)