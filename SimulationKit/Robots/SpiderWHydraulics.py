from SimulationKit.MultiBody import MultiBody
from SimulationKit.helpers import *
from SimulationKit.pubsub import *
from math import *
import ode

# Convenience multipliers...
deg2rad    = pi/180
psi2pascal = 6894.76
inch2meter = 2.54e-2
pound2kilo = 0.455

class ActuatorCharacteristics(object):
    """
    This describes the placement of a linear actuator relative to the joint it
    is controlling.  It also provides convenience trig functions for figuring
    out things like joint limits based on actuator extension.
    """
    def __init__(self):
        self.BORE_DIAMETER          = 0.0
        self.ROD_DIAMETER           = 0.0
        self.ACT_RETRACTED_LEN      = 0.1
        self.ACT_EXTENDED_LEN       = 0.1
        self.PIVOT1_DIST_FROM_JOINT = 0.1
        self.PIVOT2                 = (0.0,0.0)
        self.AXIS                   = (0,0,1)
        self.ANG_OFFSET             = 0.0
        self.SYSTEM_PRESSURE        = 2000*psi2pascal
    def getRangeOfMotion( self ):
        """Returns an angle in radians"""
        assert abs(len2(self.PIVOT2)-self.PIVOT1_DIST_FROM_JOINT) <\
            self.ACT_RETRACTED_LEN, 'You can retract in to singularity'
        retracted_angle = thetaFromABC(\
            self.PIVOT1_DIST_FROM_JOINT,\
            len2(self.PIVOT2),\
            self.ACT_RETRACTED_LEN)
        assert len2(self.PIVOT2)+self.PIVOT1_DIST_FROM_JOINT >\
            self.ACT_EXTENDED_LEN, 'You can extend in to singularity'
        extended_angle = thetaFromABC(\
            self.PIVOT1_DIST_FROM_JOINT,\
            len2(self.PIVOT2),\
            self.ACT_EXTENDED_LEN)
        assert extended_angle>retracted_angle, \
            "This actuator placement breaks sign conventions\
            ... actuator extend should increase joint angle"
        return extended_angle - retracted_angle
    def getExtensionCrossSectionM2( self ):
        """Returns piston cross sectional area in m^2 on the extend side of the
        piston"""
        return ((self.BORE_DIAMETER/2)**2)*pi
    def getRetractionCrossSectionM2( self ):
        """Returns piston cross sectional area in m^2 on the extend side of the
        piston"""
        return ((self.BORE_DIAMETER/2)**2-(self.ROD_DIAMETER/2)**2)*pi
    def getMaxExtensionForceNewtons( self ):
        """Pressure is in Newtons/sq. meter.  Returned force is in Newtons"""
        return self.getExtensionCrossSectionM2()*self.SYSTEM_PRESSURE
    def getMaxRetractionForceNewtons( self, pressure = 0.0 ):
        """Pressure is in Newtons/sq. meter.  Returned force is in Newtons"""
        return self.getRetractionCrossSectionM2()*self.SYSTEM_PRESSURE

class StompyLegPhysicalCharacteristics(object):
    """
    This class contains the physical characteristics of one of
    Stompy's legs
    """
    def __init__(self):
        self.YAW_L   = inch2meter*8.0  # Length of yaw link
        self.YAW_W   = 0.2             # Diameter of yaw link
        self.THIGH_L = inch2meter*61.0 # Length of thigh link
        self.THIGH_W = 0.2             # Diameter of thigh link
        self.CALF_L  = inch2meter*84.0 # Length of calf link
        self.CALF_W  = 0.2             # Diameter of calf link
        self.YAW_M   = pound2kilo*20   # Yaw link mass
        self.THIGH_M = pound2kilo*200  # Thigh link mass
        self.CALF_M  = pound2kilo*150  # Calf link mass

        # Describe the actuator placements at each joint
        self.YAW_ACT                          = ActuatorCharacteristics()
        self.YAW_ACT.BORE_DIAMETER            = inch2meter*2.5
        self.YAW_ACT.ROD_DIAMETER             = inch2meter*1.125
        self.YAW_ACT.ACT_RETRACTED_LEN        = inch2meter*14.25
        self.YAW_ACT.ACT_EXTENDED_LEN         = inch2meter*18.25
        self.YAW_ACT.PIVOT1_DIST_FROM_JOINT   = inch2meter*16.18
        self.YAW_ACT.PIVOT2                   = (inch2meter*2.32,inch2meter*3.3)
        self.YAW_ACT.ANG_OFFSET               = deg2rad*-30.0
        self.YAW_ACT.SYSTEM_PRESSURE          = psi2pascal*2000
        self.YAW_ACT.AXIS                     = (0,0,-1)

        self.PITCH_ACT                        = ActuatorCharacteristics()
        self.PITCH_ACT.BORE_DIAMETER          = inch2meter*3.0
        self.PITCH_ACT.ROD_DIAMETER           = inch2meter*1.5
        self.PITCH_ACT.ACT_RETRACTED_LEN      = inch2meter*20.250
        self.PITCH_ACT.ACT_EXTENDED_LEN       = inch2meter*30.250
        self.PITCH_ACT.PIVOT1_DIST_FROM_JOINT = inch2meter*7.806
        self.PITCH_ACT.PIVOT2                 = (inch2meter*25.29, inch2meter*10.21)
        self.PITCH_ACT.ANG_OFFSET             = deg2rad*-81.5
        self.PITCH_ACT.SYSTEM_PRESSURE        = psi2pascal*2000
        self.PITCH_ACT.AXIS                   = (0,-1,0)

        self.KNEE_ACT                         = ActuatorCharacteristics()
        self.KNEE_ACT.BORE_DIAMETER           = inch2meter*2.5
        self.KNEE_ACT.ROD_DIAMETER            = inch2meter*1.25
        self.KNEE_ACT.ACT_RETRACTED_LEN       = inch2meter*22.250
        self.KNEE_ACT.ACT_EXTENDED_LEN        = inch2meter*34.250
        self.KNEE_ACT.PIVOT1_DIST_FROM_JOINT  = inch2meter*28
        self.KNEE_ACT.PIVOT2                  = (inch2meter*4.3,inch2meter*6.17)
        self.KNEE_ACT.ANG_OFFSET              = deg2rad*61.84
        self.KNEE_ACT.SYSTEM_PRESSURE         = psi2pascal*2000
        self.KNEE_ACT.AXIS                    = (0,-1,0)

        # Compliance of foot
        self.COMPLIANCE_K   = 87560  # newtons/meter deflection of foot = 1000 pounds/2 inches
        self.COMPLIANCE_LEN = 0.06  # how long til it bottoms out
        # Leg origin from robot origin, expressed in Stompy's coordinate frame
        self.OFFSET_FROM_ROBOT_ORIGIN   = (0,0,0)
        # Row major 3x3 rotation matrix
        # calcRotMatrix takes an axis and an angle
        self.ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), 0.0 )
    def setRotation( self, axis, angle ):
        """
        Sets the rotation of the leg in space.
        Axis is a 3-vector, angle is a scalar in radians
        """
        rot_matrix = calcRotMatrix( axis, angle )
        self.ROTATION_FROM_ROBOT_ORIGIN = rot_matrix

class StompyPhysicalCharacteristics(object):
    """
    This class is a container for Stompy's physical layout, including
    link lengths, masses, offsets, actuator placements...
    """
    def __init__(self):
        self.BODY_W  = 2.5 
        self.BODY_T  = 0.75 # Thickness of the body capsule TODO: improve body model
        self.BODY_M  = pound2kilo*2000
        self.LEGS = []
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( (0,0,1), pi/6.0 )
        r_60z = calcRotMatrix( (0,0,1), pi/3.0 )
        r_90z = calcRotMatrix( (0,0,1), pi/2.0 )
        # To start with, the layout of the body is perfectly hexagonal
        leg_angle  = pi/6.0
        # Set their offsets and rotations from robot origin
        for i in range(6):
            leg = StompyLegPhysicalCharacteristics()
            leg.ROTATION_FROM_ROBOT_ORIGIN = calcRotMatrix( (0,0,1), leg_angle )
            leg_angle += pi/3.0
            self.LEGS.append(leg)
        self.LEGS[0].OFFSET_FROM_ROBOT_ORIGIN = mul3(( 54, 24,-12),inch2meter)
        self.LEGS[1].OFFSET_FROM_ROBOT_ORIGIN = mul3((  0, 30,-12),inch2meter)
        self.LEGS[2].OFFSET_FROM_ROBOT_ORIGIN = mul3((-54, 24,-12),inch2meter)
        self.LEGS[3].OFFSET_FROM_ROBOT_ORIGIN = mul3((-54,-24,-12),inch2meter)
        self.LEGS[4].OFFSET_FROM_ROBOT_ORIGIN = mul3((  0,-30,-12),inch2meter)
        self.LEGS[5].OFFSET_FROM_ROBOT_ORIGIN = mul3(( 54,-24,-12),inch2meter)

class SpiderWHydraulics(MultiBody):
    def __init__( self, *args, **kwargs ):
        self.dimensions = StompyPhysicalCharacteristics()
        super(self.__class__, self).__init__(*args, **kwargs)
    def buildBody( self ):
        """ Build a hexapod according to the dimensions laid out
        in self.dimensions """
        self.core = self.addBody( (self.dimensions.BODY_W/2,0,0),\
            (-1*self.dimensions.BODY_W/2,0,0),\
            self.dimensions.BODY_T,\
            mass=self.dimensions.BODY_M )

        self.publisher.addToCatalog(\
            "body.totalflow_gpm",\
            self.getTotalHydraulicFlowGPM)

        # Start another rotation
        self.legs                  = [0,0,0,0,0,0]
        for i in range(6):
            yaw_act_dim   = self.dimensions.LEGS[i].YAW_ACT
            pitch_act_dim = self.dimensions.LEGS[i].PITCH_ACT
            knee_act_dim  = self.dimensions.LEGS[i].KNEE_ACT
            hip_offset    = self.dimensions.LEGS[i].OFFSET_FROM_ROBOT_ORIGIN
            leg_rot       = self.dimensions.LEGS[i].ROTATION_FROM_ROBOT_ORIGIN
            # Anchor of the hip yaw
            yaw_p         = hip_offset
            # Anchor of the hip pitch
            hip_p         = mul3( (1,0,0), self.dimensions.LEGS[i].YAW_L )
            hip_p         = rotateAxisAngle( hip_p, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            hip_p         = rotate3( leg_rot, hip_p )
            hip_p         = add3(hip_p, yaw_p)
            # Anchor of the knee
            knee_p         = mul3( (1,0,0), self.dimensions.LEGS[i].THIGH_L )
            knee_p         = rotateAxisAngle( knee_p, \
                pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
            knee_p         = rotateAxisAngle( knee_p, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            knee_p         = rotate3( leg_rot, knee_p )
            knee_p         = add3(knee_p, hip_p)
            # Anchor of the foot
            foot_p         = mul3( (1,0,0), self.dimensions.LEGS[i].CALF_L )
            foot_p         = rotateAxisAngle( foot_p, \
                knee_act_dim.AXIS, -knee_act_dim.ANG_OFFSET )
            foot_p         = rotateAxisAngle( foot_p, \
                pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
            foot_p         = rotateAxisAngle( foot_p, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            foot_p         = rotate3( leg_rot, foot_p )
            foot_p         = add3(foot_p, knee_p)
            # Calculate the middle of the shin so we can place our shock joint
            midshin_p = div3(add3(foot_p, knee_p), 2)

            # Add hip yaw
            act_axis = rotate3(leg_rot,yaw_act_dim.AXIS)
            yaw_link = self.addBody( \
                p1     = yaw_p, \
                p2     = hip_p, \
                radius = self.dimensions.LEGS[i].YAW_W, \
                mass   = self.dimensions.LEGS[i].YAW_M )
            hip_yaw = self.addLinearVelocityActuatedHingeJoint( \
                body1  = self.core,\
                body2  = yaw_link,\
                anchor = yaw_p,\
                axis   = act_axis,\
                a1x    = yaw_act_dim.PIVOT1_DIST_FROM_JOINT,\
                a2x    = yaw_act_dim.PIVOT2[0],\
                a2y    = yaw_act_dim.PIVOT2[1])
            hip_yaw.setParam(ode.ParamLoStop, 0.0)
            hip_yaw.setParam(ode.ParamHiStop, yaw_act_dim.getRangeOfMotion())
            hip_yaw.setExtendForceLimit(yaw_act_dim.getMaxExtensionForceNewtons())
            hip_yaw.setRetractForceLimit(yaw_act_dim.getMaxRetractionForceNewtons())
            hip_yaw.setExtendCrossSection(yaw_act_dim.getExtensionCrossSectionM2())
            hip_yaw.setRetractCrossSection(yaw_act_dim.getRetractionCrossSectionM2())
            hip_yaw.setAngleOffset(yaw_act_dim.ANG_OFFSET )

            # Add thigh and hip pitch
            # Calculate the axis of rotation for hip pitch
            act_axis   = rotateAxisAngle( pitch_act_dim.AXIS, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            act_axis = rotate3(leg_rot,act_axis)
            thigh = self.addBody(\
                p1     = hip_p, \
                p2     = knee_p, \
                radius = self.dimensions.LEGS[i].THIGH_W, \
                mass   = self.dimensions.LEGS[i].THIGH_M )
            hip_pitch = self.addLinearVelocityActuatedHingeJoint( \
                body1  = yaw_link, \
                body2  = thigh, \
                anchor = hip_p, \
                axis   = act_axis, \
                a1x    = pitch_act_dim.PIVOT1_DIST_FROM_JOINT,\
                a2x    = pitch_act_dim.PIVOT2[0],\
                a2y    = pitch_act_dim.PIVOT2[1])
            hip_pitch.setParam(ode.ParamLoStop, 0.0)
            hip_pitch.setParam(ode.ParamHiStop, pitch_act_dim.getRangeOfMotion())
            hip_pitch.setExtendForceLimit(pitch_act_dim.getMaxExtensionForceNewtons())
            hip_pitch.setRetractForceLimit(pitch_act_dim.getMaxRetractionForceNewtons())
            hip_pitch.setExtendCrossSection(pitch_act_dim.getExtensionCrossSectionM2())
            hip_pitch.setRetractCrossSection(pitch_act_dim.getRetractionCrossSectionM2())
            hip_pitch.setAngleOffset(pitch_act_dim.ANG_OFFSET )

            # Add calf and knee bend
            act_axis   = rotateAxisAngle( knee_act_dim.AXIS, \
                pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
            act_axis   = rotateAxisAngle( act_axis, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            act_axis = rotate3(leg_rot,act_axis)
            calf = self.addBody( \
                p1     = knee_p, \
                p2     = midshin_p, \
                radius = self.dimensions.LEGS[i].CALF_W, \
                mass   = self.dimensions.LEGS[i].CALF_M/2.0 )
            knee_pitch = self.addLinearVelocityActuatedHingeJoint( \
                body1  = thigh, \
                body2  = calf, \
                anchor = knee_p, \
                axis   = act_axis, \
                a1x    = knee_act_dim.PIVOT1_DIST_FROM_JOINT,\
                a2x    = knee_act_dim.PIVOT2[0],\
                a2y    = knee_act_dim.PIVOT2[1])
            knee_pitch.setParam(ode.ParamLoStop, 0.0)
            knee_pitch.setParam(ode.ParamHiStop, knee_act_dim.getRangeOfMotion())
            knee_pitch.setExtendForceLimit(knee_act_dim.getMaxExtensionForceNewtons())
            knee_pitch.setRetractForceLimit(knee_act_dim.getMaxRetractionForceNewtons())
            knee_pitch.setExtendCrossSection(knee_act_dim.getExtensionCrossSectionM2())
            knee_pitch.setRetractCrossSection(knee_act_dim.getRetractionCrossSectionM2())
            knee_pitch.setAngleOffset(knee_act_dim.ANG_OFFSET )

            # Create the foot
            # Add the compliant joint
            act_axis   = rotateAxisAngle( knee_act_dim.AXIS, \
                knee_act_dim.AXIS, -knee_act_dim.ANG_OFFSET )
            act_axis   = rotateAxisAngle( act_axis, \
                pitch_act_dim.AXIS, -pitch_act_dim.ANG_OFFSET )
            act_axis   = rotateAxisAngle( act_axis, \
                yaw_act_dim.AXIS, -yaw_act_dim.ANG_OFFSET )
            act_axis = rotate3(leg_rot,act_axis)
            foot = self.addBody( \
                p1     = midshin_p, \
                p2     = foot_p, \
                radius = self.dimensions.LEGS[i].CALF_W, \
                mass   = self.dimensions.LEGS[i].CALF_M/2 )
            calf_axis  = norm3(sub3(midshin_p, foot_p))
            foot_shock = self.addPrismaticSpringJoint( \
                body1        = calf, \
                body2        = foot, \
                axis         = mul3(calf_axis,-1),\
                spring_const = -80e3,\
                hi_stop      = 0.1,\
                lo_stop      = 0.0,\
                neutral_position = 0.0,\
                damping          = -1e1)
            def populatePublisher( dof_name, joint ):
                self.publisher.addToCatalog(\
                    "l%d.%s.torque"%(i,dof_name),\
                    joint.getTorque)
                self.publisher.addToCatalog(\
                    "l%d.%s.torque_lim"%(i,dof_name),\
                    joint.getTorqueLimit)
                self.publisher.addToCatalog(\
                    "l%d.%s.ang"%(i,dof_name),\
                    joint.getAngle)
                self.publisher.addToCatalog(\
                    "l%d.%s.len"%(i,dof_name),\
                    joint.getLength)
                self.publisher.addToCatalog(\
                    "l%d.%s.len_rate"%(i,dof_name),\
                    joint.getLengthRate)
                self.publisher.addToCatalog(\
                    "l%d.%s.flow_gpm"%(i,dof_name),\
                    joint.getHydraulicFlowGPM)
                self.publisher.addToCatalog(\
                    "l%d.%s.lever_arm"%(i,dof_name),\
                    joint.getLeverArm)
                self.publisher.addToCatalog(\
                    "l%d.%s.extend_force"%(i,dof_name),\
                    joint.getExtendForceLimit)
                self.publisher.addToCatalog(\
                    "l%d.%s.retract_force"%(i,dof_name),\
                    joint.getRetractForceLimit)
            populatePublisher('hy', hip_yaw)
            populatePublisher('hp', hip_pitch)
            populatePublisher('kp', knee_pitch)
                
            d                 = {}
            d['hip_yaw']      = hip_yaw
            d['hip_pitch']    = hip_pitch
            d['knee_pitch']   = knee_pitch
            d['foot_shock']   = foot_shock
            d['hip_yaw_link'] = yaw_link
            d['thigh']        = thigh
            d['calf']         = calf
            d['foot']         = foot
            self.legs[i]      = d
    def getEncoderAngleMatrix( self ):
        """
        Returns a list of tuples containing the joint angles at each joint.
        Outer index is leg index
        Inner index is joint index
        So retval[0][0] is hip yaw for leg 0,
        retval[1][0] is hip yaw for leg 1,
        retval[0][2] is knee angle for leg 0, etc.
        """
        retval = []
        for i in range(6):
            retval.append( (\
                self.legs[i]['hip_yaw'].getAngle(),\
                self.legs[i]['hip_pitch'].getAngle(),\
                self.legs[i]['knee_pitch'].getAngle(),\
                self.legs[i]['foot_shock'].getPosition()) )
        return retval
    def setLenRateMatrix( self, len_rate_matrix ):
        """
        Provides an interface to set the length rates of the actuators
        at all joints at the same time.
        len_rate_matrix outer indices are leg indices
        inner indices specify joints
        len_rate_matrix[0][1] is leg 0 hip pitch
        len_rate_matrix[1][2] is leg 1 knee pitch
        """
        for i in range(6):
            self.legs[i]['hip_yaw'   ].setLengthRate(len_rate_matrix[i][0])
            self.legs[i]['hip_pitch' ].setLengthRate(len_rate_matrix[i][1])
            self.legs[i]['knee_pitch'].setLengthRate(len_rate_matrix[i][2])
    def getTotalHydraulicFlowGPM( self ):
        total = 0
        for i in range(6):
            total += abs(self.legs[i]['hip_yaw'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['hip_pitch'].getHydraulicFlowGPM())
            total += abs(self.legs[i]['knee_pitch'].getHydraulicFlowGPM())
        return total
    def setDesiredFootPositions( self, positions ):
        """
        positions should be an iterable of 6 positions relative to the body
        """
        # These are the rotation matrices we will use
        i = 0

        for target_p in positions:
            yaw_p = self.dimensions.LEGS[i].OFFSET_FROM_ROBOT_ORIGIN
            # Move the target point from the robot coordinate frame
            # to the leg coordinate frame
            target_p         = sub3(target_p, yaw_p)
            rot              = invert3x3(self.dimensions.LEGS[i].ROTATION_FROM_ROBOT_ORIGIN)
            target_p         = rotate3( rot, target_p )
            # Calculate hip yaw target angle
            hip_yaw_angle    = atan2( target_p[1], target_p[0] )
            # Move target_p to the coordinate frame based at hip pitch
            target_p = rotateAxisAngle( target_p,\
                self.dimensions.LEGS[i].YAW_ACT.AXIS, hip_yaw_angle )
            target_p         = sub3( target_p, (self.dimensions.LEGS[i].YAW_L,0,0) )
            # Assign outputs
            # Calculate leg length
            leg_l            = len3( target_p )
            # Use law of cosines on leg length to calculate knee angle 
            knee_angle       = pi-thetaFromABC( self.dimensions.LEGS[i].THIGH_L, self.dimensions.LEGS[i].CALF_L, leg_l )
            # Calculate hip pitch
            knee_comp_angle  = thetaFromABC( leg_l, self.dimensions.LEGS[i].THIGH_L, self.dimensions.LEGS[i].CALF_L )
            depression_angle = -atan2(target_p[2], target_p[0])
            hip_pitch_angle  = depression_angle-knee_comp_angle
            def controlLenRate( joint, target_ang, gain=10.0 ):
                error = target_ang - joint.getAngle()
                joint.setLengthRate( error*gain )
            controlLenRate(self.legs[i]['hip_yaw'   ],  hip_yaw_angle   )
            controlLenRate(self.legs[i]['hip_pitch' ],  hip_pitch_angle )
            controlLenRate(self.legs[i]['knee_pitch'],  knee_angle      )
            i+=1
    def getBodyHeight( self ):
        return self.core.getPosition()[2]
    def getPosition( self ):
        return self.core.getPosition()
    def getAcceleration( self ):
        return div3(self.core.getForce(), self.dimensions.BODY_M) # FIXME: Returns (0,0,0)
    def getOrientation( self ):
        return self.core.getRotation()
    def getAngularRates( self ):
        return self.core.getAngularVel()
    def getVelocity( self ):
        return self.core.getLinearVel()
    def constantSpeedWalk( self ):
        gait_cycle      = 3.0     # time in seconds
        step_cycle      = gait_cycle/2.0
        swing_overshoot = 1.00
        stride_length   = 1.70    # length of a stride, m
        body_h          = 2.00    # height of body off the ground, m
        foot_lift_h     = 0.25    # how high to lift feet in m

        foot_positions = []
        x_off_swing  =  swing_overshoot*(stride_length/2.0)*cos(2*pi*(self.sim.sim_t%step_cycle)/gait_cycle)
        x_off_stance =  stride_length*(((self.sim.sim_t%step_cycle)/step_cycle)-0.5)
        z_off        =  foot_lift_h*sin(2*pi*self.sim.sim_t/gait_cycle)
        if z_off<0:
            z_off *= -1
        for i in range(6):
            # Neutral position in the leg coordinate frame
            neutral_pos = (inch2meter*70, 0, -inch2meter*60)
            tmp = rotate3( self.dimensions.LEGS[i].ROTATION_FROM_ROBOT_ORIGIN, neutral_pos )
            x, y, z = add3( tmp, self.dimensions.LEGS[i].OFFSET_FROM_ROBOT_ORIGIN )
            if (i%2) ^ (self.sim.sim_t%gait_cycle<(step_cycle)):
                x += x_off_swing
                z += z_off
            else:
                x += x_off_stance
            p = ( x, y, z )
            foot_positions.append(p)
        self.setDesiredFootPositions( foot_positions )
        return foot_positions
    def colorShockByDeflection( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getPosition()/joint.getHiStop())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorJointByTorque( self, joint ):
            b = joint.getBody(1)
            r = abs(joint.getTorque()/joint.getTorqueLimit())
            if r >= 0.99:
                b.color = (0,0,0,255)
            else:
                b.color = (255*r,255*(1-r),0,255)
    def colorTorque( self ):
        for i in range(6):
            # Color overtorque
            self.colorJointByTorque(     self.legs[i]['hip_yaw'] )
            self.colorJointByTorque(     self.legs[i]['hip_pitch'] )
            self.colorJointByTorque(     self.legs[i]['knee_pitch'] )
            self.colorShockByDeflection( self.legs[i]['foot_shock'])
    def update( self ):
        MultiBody.update(self)
