#from inputs import devices
from inputs import get_gamepad
import time
from threading import Thread
import sys
sys.path.append('../galatae-api/')
from robot import Robot
import math

buttons=["ABS_X","ABS_Y","ABS_RX","ABS_RY","BTN_DPAD_LEFT","BTN_DPAD_RIGHT","BTN_DPAD_DOWN","BTN_DPAD_UP","BTN_WEST","BTN_EAST","BTN_SOUTH","BTN_NORTH","BTN_SELECT","BTN_START"]

joystick_pos=[0.0] * len(buttons)

def normalize(v):
    normVal=v/127.0-1
    threshold=0.5
    if(-threshold <= normVal and normVal<=threshold):
      normVal=0.0

    return normVal

def updateJoystickValues():
  while True:
    events = get_gamepad()
    for event in events:
      if(event.code in buttons):
        index=buttons.index(event.code)
        if(index<4):
          joystick_pos[index]=normalize(event.state)
        else:
          joystick_pos[index]=event.state
    time.sleep(0.001)

def get_jog_dir(gripper_is_open):
  jog_dir=[0] * 6

  abs_speed=2
  btn_speed=0.5

  jog_dir[0]=joystick_pos[1]*abs_speed
  jog_dir[1]=joystick_pos[0]*abs_speed
  jog_dir[2]=-joystick_pos[3]*abs_speed
  jog_dir[3]=(joystick_pos[7]-joystick_pos[6])*btn_speed
  jog_dir[4]=(joystick_pos[4]-joystick_pos[5])*btn_speed
  jog_dir[5]=0.0
  if(not gripper_is_open):
    jog_dir[5]=0.0
  
  return jog_dir


def ps_control():
  r=Robot(False)
  #r.set_tool([0,0,0])
  thread=Thread(target=updateJoystickValues)
  thread.start()

  gripper_is_open=True
  number_of_jog_buttons=8
  start_pose=[400,0,150,180,0]

  print("start calibration")
  r.reset_and_home_joints()
  print("cal ok")
  r.set_joint_speed(50)
  r.go_to_pose(start_pose)

  print("ready!")

  while True:
    if not all(x == 0 or x == 0.0 for x in joystick_pos[:number_of_jog_buttons]):
      r.jog(get_jog_dir(gripper_is_open))
      print(r.get_tool_pose())
    elif(joystick_pos[10]==1):
      r.close_gripper()
      gripper_is_open=False
    elif(joystick_pos[11]==1 and not gripper_is_open):
      r.open_gripper()
      gripper_is_open=True
    elif(joystick_pos[12]==1):
      r.go_to_foetus_pos()
    elif(joystick_pos[13]==1):
      r.go_to_pose(start_pose)

    #print lz position du robot
    #r.get_pose()
    time.sleep(0.0001)

def check_ps_buttons():
  while True:	# loop for ever
    for event in get_gamepad():	# check events of gamepads, if not event, all is stop
      if event.ev_type == "Key":	# category of binary respond values
        print(event.code,": ",event.state)
        
def main():
  ps_control()
  #check_ps_buttons()
  #test()

if __name__ == "__main__":
  main()