#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# we wish to calculate the difference in stopping distance between v1 (leader)
# and v2 (follower), given their initial velocities, deceleration rates, and
# the delay between the leader starting to decelerate and the follower doing
# so.

# stopping distance for v1 is calculated with:
# d = vt + 1/2at^2
# t = abs(v/a)
# d = v^2/a + 1/2a(v^2/a^2) -- (abs not shown)
# since a is negative, this reduces to
# d = -1/2(v^2/a)

# stopping distance for v2 is the same, but also includes the distance traveled
# during the delay (b), before deceleration starts
# d = v*b - 1/2(v^2/a)

def distance(v1_vel, v2_vel, v1_dec, v2_dec, delay):
  return (v2_vel*delay - (1.0/2.0*(v2_vel**2/v2_dec))) - (-1.0/2.0*(v1_vel**2/v1_dec))

# start some test plots, assuming starting values as follows:
# initial velocities: 29m/s
# decel rates: -9.0m/s^2
# decel delay: .5s

v1_initial_velocity = v2_initial_velocity = 29.0
v1_initial_decel = v2_initial_decel = -9.0
initial_decel_delay = 0.5
velocity_range = np.linspace(20, 35, 91)
decel_range = np.linspace(-6, -11, 51)
delay_range = np.linspace(0, 1, 101)

#distance_threshold = (v2_initial_velocity*initial_decel_delay - (1.0/2.0*(v2_initial_velocity**2/v2_initial_decel))) - (-1.0/2.0*(v1_initial_velocity**2/v1_initial_decel))

v1_velocity = v1_initial_velocity
v2_velocity = v2_initial_velocity
v1_decel = v1_initial_decel
v2_decel = v2_initial_decel
decel_delay = initial_decel_delay

def distance_for_v1_vel():
  return [distance(v1_temp_velocity, v2_velocity, v1_decel, v2_decel, decel_delay) for v1_temp_velocity in velocity_range]
def distance_for_v2_vel():
  return [distance(v1_velocity, v2_temp_velocity, v1_decel, v2_decel, decel_delay) for v2_temp_velocity in velocity_range]
def distance_for_v1_dec():
  return [distance(v1_velocity, v2_velocity, v1_temp_decel, v2_decel, decel_delay) for v1_temp_decel in decel_range]
def distance_for_v2_dec():
  return [distance(v1_velocity, v2_velocity, v1_decel, v2_temp_decel, decel_delay) for v2_temp_decel in decel_range]
def distance_for_delay():
  return [distance(v1_velocity, v2_velocity, v1_decel, v2_decel, decel_temp_delay) for decel_temp_delay in delay_range]


# plots will look like the following:
# /-----------------\
# | v1_vel | v2_vel |
# |--------+--------|
# | v1_dec | v2_dec |
# |--------+--------|
# |      delay      |
# \-----------------/

# misc
plt.subplots_adjust(bottom=0.35)
axcolor = 'lightgoldenrodyellow'

# v1 initial velocity varies
x = velocity_range
y = distance_for_v1_vel()
plt.subplot(3,2,1)
v1_vel_plot, = plt.plot(x,y)
plt.ylabel("distance (m)")
plt.xlabel("v1 initial velocity (m/s)")

# v2 initial velocity varies
x = velocity_range
y = distance_for_v2_vel()
plt.subplot(3,2,2)
v2_vel_plot, = plt.plot(x,y)
plt.ylabel("distance (m)")
plt.xlabel("v2 initial velocity (m/s)")

# v1 deceleration varies
x = decel_range
y = distance_for_v1_dec()
plt.subplot(3,2,3)
v1_dec_plot, = plt.plot(x,y)
plt.ylabel("distance")
plt.xlabel("v1 deceleration (m/s^2)")

# v2 deceleration varies
x = decel_range
y = distance_for_v2_dec()
plt.subplot(3,2,4)
v2_dec_plot, = plt.plot(x,y)
plt.ylabel("distance")
plt.xlabel("v2 deceleration (m/s^2)")

# deceleration delay varies
x = delay_range
y = distance_for_delay()
plt.subplot(3,2,4)
plt.subplot(3,1,3)
delay_plot, = plt.plot(x,y)
plt.ylabel("distance")
plt.xlabel("delay before v2 decelerates (s)")

# Sliders
axv1vel = plt.axes([.25, 0.25, 0.5, 0.03], facecolor=axcolor)
s_v1vel = Slider(axv1vel, "v1 Velocity", 20, 35, valinit=v1_initial_velocity)
axv2vel = plt.axes([.25, 0.20, 0.5, 0.03], facecolor=axcolor)
s_v2vel = Slider(axv2vel, "v2 Velocity", 20, 35, valinit=v2_initial_velocity)
axv1dec = plt.axes([.25, 0.15, 0.5, 0.03], facecolor=axcolor)
s_v1dec = Slider(axv1dec, "v1 Decel", -11, -6, valinit=v1_initial_decel)
axv2dec = plt.axes([.25, 0.10, 0.5, 0.03], facecolor=axcolor)
s_v2dec = Slider(axv2dec, "v2 Decel", -11, -6, valinit=v2_initial_decel)
axdelay = plt.axes([.25, 0.05,  0.5, 0.03], facecolor=axcolor)
s_delay = Slider(axdelay, "Delay", 0, 1, valinit=initial_decel_delay)

def update(val):
  global v1_velocity
  global v2_velocity
  global v1_decel
  global v2_decel
  global decel_delay 
  v1_velocity = s_v1vel.val
  v2_velocity = s_v2vel.val
  v1_decel    = s_v1dec.val
  v2_decel    = s_v2dec.val
  decel_delay = s_delay.val
  v1_vel_plot.set_ydata(distance_for_v1_vel())
  v2_vel_plot.set_ydata(distance_for_v2_vel())
  v1_dec_plot.set_ydata(distance_for_v1_dec())
  v2_dec_plot.set_ydata(distance_for_v2_dec())
  delay_plot.set_ydata(distance_for_delay())
s_v1vel.on_changed(update)
s_v2vel.on_changed(update)
s_v1dec.on_changed(update)
s_v2dec.on_changed(update)
s_delay.on_changed(update)

plt.show()


