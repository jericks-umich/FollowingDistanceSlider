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
distance_val = distance(v1_velocity, v2_velocity, v1_decel, v2_decel, decel_delay)

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


# initialization
fig, ax1 = plt.subplots()
plt.subplots_adjust(bottom=0.40)
ax1.set_ylabel("Minimum initial separation distance (m): %2.2f" % distance_val)

ax1.set_xlabel("Velocity (m/s)")
x = velocity_range
# v1 initial velocity varies
y = distance_for_v1_vel()
v1_vel_plot, = ax1.plot(x,y, color='blue')
v1_vel_dot, = ax1.plot(v1_velocity, distance_val, 'o', color='blue')
# v2 initial velocity varies
y = distance_for_v2_vel()
v2_vel_plot, = ax1.plot(x,y, color='green')
v2_vel_dot, = ax1.plot(v2_velocity, distance_val, 'o', color='green')

ax2 = ax1.twiny() # create a second plot using the same x-axis

ax2.set_xlabel("Deceleration (m/s^2)")
x = decel_range
# v1 deceleration varies
y = distance_for_v1_dec()
v1_dec_plot, = ax2.plot(x,y, color='red')
v1_dec_dot, = ax2.plot(v1_decel, distance_val, 'o', color='red')
# v2 deceleration varies
y = distance_for_v2_dec()
v2_dec_plot, = ax2.plot(x,y, color='cyan')
v2_dec_dot, = ax2.plot(v2_decel, distance_val, 'o', color='cyan')

ax3 = ax1.twiny() # create third plot
ax3.get_xaxis().set_visible(False)
x = delay_range
# deceleration delay varies
y = distance_for_delay()
delay_plot, = ax3.plot(x,y, color='magenta')
delay_dot, = ax3.plot(decel_delay, distance_val, 'o', color='magenta')

# Sliders
axv1vel = plt.axes([.15, 0.25, 0.7, 0.03], facecolor='blue')
s_v1vel = Slider(axv1vel, "v1 Velocity", 20, 35, valinit=v1_initial_velocity)
axv2vel = plt.axes([.15, 0.20, 0.7, 0.03], facecolor='green')
s_v2vel = Slider(axv2vel, "v2 Velocity", 20, 35, valinit=v2_initial_velocity)
axv1dec = plt.axes([.15, 0.15, 0.7, 0.03], facecolor='red')
s_v1dec = Slider(axv1dec, "v1 Decel", 6, 11, valinit=-v1_initial_decel)
axv2dec = plt.axes([.15, 0.10, 0.7, 0.03], facecolor='cyan')
s_v2dec = Slider(axv2dec, "v2 Decel", 6, 11, valinit=-v2_initial_decel)
axdelay = plt.axes([.15, 0.05, 0.7, 0.03], facecolor='magenta')
s_delay = Slider(axdelay, "Delay", 0, 1, valinit=initial_decel_delay)

def update(val):
  global v1_velocity
  global v2_velocity
  global v1_decel
  global v2_decel
  global decel_delay
  v1_velocity  = s_v1vel.val
  v2_velocity  = s_v2vel.val
  v1_decel     = -s_v1dec.val
  v2_decel     = -s_v2dec.val
  decel_delay  = s_delay.val
  distance_val = distance(v1_velocity, v2_velocity, v1_decel, v2_decel, decel_delay)
  v1_vel_plot.set_ydata(distance_for_v1_vel())
  v2_vel_plot.set_ydata(distance_for_v2_vel())
  v1_dec_plot.set_ydata(distance_for_v1_dec())
  v2_dec_plot.set_ydata(distance_for_v2_dec())
  delay_plot.set_ydata(distance_for_delay())
  v1_vel_dot.set_ydata(distance_val)
  v1_vel_dot.set_xdata(v1_velocity)
  v2_vel_dot.set_ydata(distance_val)
  v2_vel_dot.set_xdata(v2_velocity)
  v1_dec_dot.set_ydata(distance_val)
  v1_dec_dot.set_xdata(v1_decel)
  v2_dec_dot.set_ydata(distance_val)
  v2_dec_dot.set_xdata(v2_decel)
  delay_dot.set_ydata(distance_val)
  delay_dot.set_xdata(decel_delay)
  ax1.set_ylabel("Minimum initial separation distance (m): %2.2f" % distance_val)
s_v1vel.on_changed(update)
s_v2vel.on_changed(update)
s_v1dec.on_changed(update)
s_v2dec.on_changed(update)
s_delay.on_changed(update)


resetax = plt.axes([0.8, 0.001, 0.1, 0.04])
button = Button(resetax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

def reset(event):
  s_v1vel.reset()
  s_v2vel.reset()
  s_v1dec.reset()
  s_v2dec.reset()
  s_delay.reset()
button.on_clicked(reset)


plt.show()


