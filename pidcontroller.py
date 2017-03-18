import time
import matplotlib.pyplot

class Model:
    """A model of a an object heated or cooled by the ambient temperature"""

    def __init__(self, current_value, k, dt):
        self.k = k
        self.dt = dt
        self.current_value = current_value

    def water_temp_model(self, control_value):
        d_value = self.k*(control_value - self.current_value)*self.dt
        self.current_value = self.current_value + d_value
        return self.current_value

class Pid:
    """A PID controller"""

    def __init__(self, kp, ki, kd, dt, set_value, min, max, logger):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.set_value = set_value
        self.error_i = 0
        self.last_error = 0
        self.min = min
        self.max = max
        self.logger = logger

    def apply_min_max_limit(self, control_value):
        if control_value > self.max:
            return self.max
        if control_value < self.min:
            return self.min
        return control_value

    def pid(self, current_value):
        error = self.set_value - current_value
        self.error_i = self.error_i + error * self.dt
        error_d = (self.last_error - error) / self.dt
        self.last_error = error

        kp_control = error * self.kp
        ki_control = self.error_i * self.ki
        kd_control = error_d * self.kd
        control_value = kp_control + ki_control + kd_control

        control_value = self.apply_min_max_limit(control_value)

        self.logger.log(current_value, control_value)

        return control_value

class Logger:
    def __init__(self, t_max, set_value):
        self.current_value = []
        self.control_value = []
        self.time = []
        self.t_max = t_max
        self.set_value = set_value

    def log(self, current_value, control_value):
        self.current_value.append(current_value)
        self.control_value.append(control_value)

    def log_time(self, time):
        self.time.append(time)

    def plot(self):
        matplotlib.pyplot.plot(self.time, self.current_value, 'r')
        matplotlib.pyplot.plot(self.time, self.control_value, 'g')
        matplotlib.pyplot.plot([0, self.t_max],[self.set_value, self.set_value], 'b')
        matplotlib.pyplot.title("red = current value, green = control value, blue = set value")
        matplotlib.pyplot.show()

def control_loop():
    #Resources:
    #http://matplotlib.org/users/pyplot_tutorial.html
    #https://docs.python.org/3/tutorial/classes.html
    #http://pythonforphysics.blogspot.se/2013/05/1-bouncing-ball.html
    current_value = 20 #initial temperature of object
    control_value = 80 #intial temperature of heat device
    set_value = 80
    dt =  0.05
    min_control_value = 0
    max_control_value = 100
    kp = 10
    ki = 0.25
    kd = 0
    k = 0.1

    t = 0 #initial time
    t_max = 300

    logger = Logger(t_max, set_value)
    model = Model(current_value, k, dt)
    pid = Pid(kp, ki, kd, dt, set_value, min_control_value, max_control_value, logger)

    while t < t_max: #main loop
        current_value = model.water_temp_model(control_value)
        control_value = pid.pid(current_value)
        logger.log_time(t)
        t = t + dt

    logger.plot()

if __name__ == "__main__":
    control_loop()
