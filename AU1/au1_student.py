"""
Program for simulation of satellite docking between satellite 1 and
satellite 2.

Parameters:
docked = 0      # Flag for controlling if the satellites
                # have docked (docked = 1) or not (docked = 0)
                
F = 300         # Initial force affecting satellite 1
            
m1 = 500        # Mass of satellite 1
x1 = -100       # Initial position of satellite 1
v1 = 10         # Initial velocity of satellite 1

m2 = 1000       # Mass of satellite 2
x2 = 0          # Initial position of satellite 2
v2 = 0          # Initial velocity of satellite 2

dt              # Time step. Updated in each iteration and given as
                # the difference in (absolute) time between current iteration
                # and previous iteration.

Task: Modify the function update_sat so that the positions and velocities 
of the satellites are updated corrected and obeying the laws of physics.
(see further instructions inside function update_sat).

Last update
Jorgen Ekman, 13 January 2023
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time


docked = 0  # Flag for controlling if the satellites
            # have docked (docked = 1) or not (docked = 0)
t_lim = 40  # The duration in seconds the simulation lasts.
            # Should be around 40 s at hand in, but can be changed during
            # the development of the function.
def update_sat(x1,x2,v1,v2,F,dt):
    """
    Indata:
    x1 (float): position of satellite 1 at time t
    x2 (float): position of satellite 2 at time t
    v1 (float): velocity of satellite 1 at time t
    v2 (float): velocity of satellite 2 at time t
    F (float):  force affecting satellite 1 at time t
    dt (float): time step at time t
    
    Returnerar: 
    xnew1 (float): position of satellite 1 at time t + dt
    xnew2 (float): position of satellite 2 at time t + dt
    vnew1 (float): velocity of satellite 1 at time t + dt
    vnew2 (float): velocity of satellite 2 at time t + dt
    
    Task: Modify the function so that the positions and velocities of the
    satellites are uppdated correctly and obeying the laws of physics.
    If the distance between the satellites is less than 5 m, one of two things 
    will happen:
    1. If the relative velocity is less than 2 m/s, the satellites will dock, 
    which is modeled as a totally inelastic collision (fullstandigt inelastisk stot).
    2. If the relative velocity is larger than or equal to 2 m/s, the  
    satellites will bounce of each other (docking failed), 
    which is modeled as an elastic collision (elastisk stot).

    """
    global docked
    
    # Räkna ut distansen mellan satelliterna, abs returnerar absokuta värdet av ett nummer.
    distance = abs(x2 - x1)

    # Uppdatera nya positioner och hastigheter
    # v = dx/dt och flyttar om så att vi får dx=v*dt, så original positionen + nya positionen
    xnew1 = x1 + (v1 * dt)
    xnew2 = x2 + (v2 * dt)
    
    # Newtons andra lag, F=m*a --> F=m* dv/dt --> dv=(F/m)*dt
    vnew1 = v1 + (F / m1) * dt
    # bara v2 så den INTE rör på sig i början
    vnew2 = v2 
    
    # Villkor: om distans är mindre än 5m (tillräckligt nära för o dockas) --> 
    if distance < 5.0:
        relative_velocity = abs(v2 - v1)
        
        # 1. Om relativa hastighet är mindre 2/ms ska satelliterna dockas. 
        if relative_velocity < 2.0:
            docked = 1
            # Formeln tagits från föreläsning 
            # modellerar inelastisk kollision
            vnew1 = ((m1)/(m1+m2))*vnew1
            vnew2 = vnew1
        else:
            # 2. Om relativa hastighet är större/lika med 2m/s ska satelliterna bounce form each other.
            # Uppdaterar hastighet och position, formeln är vad som händer efter en elastisk kollision
            vnew1 = ((m1-m2)/(m1+m2))*v1
            xnew1 = x1 + (vnew1*dt)
            # för v2
            vnew2 = ((2*m1)/(m1+m2))*v1
            xnew2 = x2 + (vnew2*dt)
           
    return xnew1,xnew2,vnew1,vnew2

# Initialisation of some parameters (don't change)
F = 300
m1 = 500
x1 = -20
v1 = 0

m2 = 1000
x2 = 0
v2 = 0

fig, ax = plt.subplots()
# Adjust figure to make room for buttons
fig.subplots_adjust(bottom=0.25)

# Create button which decrease force with 50 N.
decrax = fig.add_axes([0.2, 0.05, 0.2, 0.08])
decr_button = Button(decrax, 'Decrease Thrust', hovercolor='0.975')

def decr(event):
    global F
    F = F - 50.0
    
decr_button.on_clicked(decr)

# Create button which increase force with 50 N.
incrax = fig.add_axes([0.65, 0.05, 0.2, 0.08])
incr_button = Button(incrax, 'Increase Thrust', hovercolor='0.975')

def incr(event):
    global F
    F = F + 50.0
    
incr_button.on_clicked(incr)

tstart = time.time()
telapsed = 0
told = tstart
# Main loop startshere
while telapsed <= t_lim:
    # Deduce time and time step
    tnew = time.time()
    dt = tnew - told
    told = tnew
    
    # Call to function update_sat
    x1,x2,v1,v2 = update_sat(x1,x2,v1,v2,F,dt)
    
    telapsed = time.time() - tstart
    
    # Update plot
    ax.plot(x1,0,'wo')
    ax.plot(x2,0,'ro',markersize=10)
    ax.set_xlabel('x (m)',fontsize=12)
    ax.set_xlim([-150,50])
    ax.set_facecolor("black")
    ax.tick_params(labelsize=12, left = False, labelleft = False)
    
    # Update text
    textstr = '\n'.join((
    'Time: %6.2f s' % (telapsed,),
    'Distance: %6.2f m' % (abs(x2-x1), ),
    'Relative  velocity: %6.2f m/s' % (abs(v2-v1), )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.25, 0.9, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
    textstr2 = ('Force: %4.1f N' % (F))
    ax.text(0.4, -0.225, textstr2, transform=ax.transAxes, fontsize=12,
        verticalalignment='top')
    
    # If succesful docking
    textstring = "Docking succesful!!"
    if docked == 1:
        ax.text(0.5, 0.2, textstring, transform=ax.transAxes, color="white", fontsize=12,
        verticalalignment='top')
        
    plt.pause(0.1)
    
    # Don't clear the last plot
    if telapsed < t_lim:
        ax.cla()
    

    
    