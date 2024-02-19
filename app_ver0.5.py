from flask import Flask, render_template, request
from adafruit_servokit import ServoKit
import atexit

app = Flask(__name__)

# Set up PCA9685 and initialize servos
kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(500, 2500)

# Define servo positions for channel 1
servo1_pos = 90  # Initial position
servo2_pos = 90

# Define servo positions for channel 2
servo3_pos = 90  # Initial position
servo4_pos = 90

# Cleanup function to stop servos on exit
def cleanup():
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90

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

@app.route('/set_midway', methods=['POST'])
def set_midway():
    midway = 90  # Midway point for servo channel 2
    kit.servo[2].angle = midway
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

