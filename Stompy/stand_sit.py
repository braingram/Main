from ControlsKit import time_sources, BodyModel, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF, array
from ControlsKit.body_paths import TrapezoidalSitStand, BodyPause, TrapezoidalFeetAlign
from UI import logger
from scipy import zeros

controller = BodyController()
model = BodyModel()
path = None
state = 0

ORIENT = 1
STAND = 2
SIT = 3

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command=None):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    target_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    #THIS IS WHERE WE CALL ON THE PATH TO DO MATH AND PRODUCE joint_angle_matrix (6x3 matrix)
    if path is None:
        path = BodyPause(model, controller, 1)
        state = ORIENT
    
    i = 0; #index variable for orienting legs
    
    if path.isDone():
        if state == ORIENT:
            path = TrapezoidalFeetAlign(model, controller, [i], [array([0, -1.4,  2.2])], 2, 1)
            i += 1
            if i == 6:
                i = 0
                state =STAND
        elif state == STAND:
            path = TrapezoidalSitStand(model, controller, -1.75, 2, 1)
            state = SIT
        elif state == SIT:
            path = TrapezoidalSitStand(model, controller, -.5, 2, 1)
            state = STAND
        elif state == 0:
            path = BodyPause(model, controller, 10)

        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    target_angle_matrix  = path.update()
    print "target_angle_matrix in stand_sit: ", target_angle_matrix
    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)
