import sys
import ac
import acsys

import SimpleFuel_sim_info

# global variables
appWindow = 0

prevlaps = 0 #for detect lap change

fuelperlap = 0
prevfuel = 0

maxlaps = 0

colors = {
    "white": [255, 255, 255],
    "yellow": [255, 255,   0],
    "green": [0, 170,   0],
    "red": [255,   0,   0],
    "orange1": [255, 80,   0],
    "orange2": [255, 160,   0],
    "black": [0,   0,   0],
    "grey": [140, 140, 140]
}

# Labels
label1 = 0

def acMain(ac_version):
    global appWindow, label1, prevlaps, prevfuel, fuelperlap

    try:
        prevlaps = 0
        fuelperlap = 0
        prevfuel = 0

        appWindow = ac.newApp("SimpleFuel")
        ac.setSize(appWindow, 200, 140)
        ac.setTitle(appWindow, "")
        ac.setIconPosition(appWindow, 0, -9000)
        ac.drawBorder(appWindow, 0)
        ac.setBackgroundOpacity(appWindow, 0)
        ac.drawBackground(appWindow, 0)

        label1 = ac.addLabel(appWindow, "remainingLabel")
        ac.setText(label1, "loading")
        ac.setFontAlignment(label1, "left")
        ac.setFontSize(label1, 30)
        ac.setPosition(label1, 0, 0)

        sim_info_obj = SimpleFuel_sim_info.fuel_usage_SimInfo()
        prevfuel = sim_info_obj.physics.fuel #first fuel measure on load

        ac.console("ac SimpleFuel loaded " )

    except Exception as f:
        ac.console("Error because shit: " % f)  # Fucking errors ;(
        
    return "SimpleFuel"


def acUpdate(deltaT):
    global appWindow, label1, prevlaps, prevfuel, fuelperlap,maxlaps

    #---------logic changes--------------

    #update sim data
    sim_info_obj = SimpleFuel_sim_info.fuel_usage_SimInfo()
    actualfuel = sim_info_obj.physics.fuel
    maxfuel = sim_info_obj.static.maxFuel
    laps = sim_info_obj.graphics.completedLaps
    box = ac.isCarInPit(0)
    trackConfiguration = ac.getTrackConfiguration(0)

    #every cycle changes
    fuelpercent = (100/maxfuel)*actualfuel

    #laps whit current fuel
    if fuelperlap > 0:
        maxlaps = actualfuel/fuelperlap 

    #if enter box update previous fuel and reset fuel per lap
    if box > 0:
        prevfuel = actualfuel
        fuelperlap = 0

    #once per lap changes
    if laps > 0:
        if prevlaps != laps:
            prevlaps = laps
            fuelperlap = prevfuel - actualfuel
            prevfuel = actualfuel

    #---------GUI changes--------------
    ac.setText(label1, "L:{0}l {1}%\nL/V:{2}l\nVres:{3}\nTrack config:\n {4}".format(round(
        actualfuel, 1), round(fuelpercent, 1), round(fuelperlap, 1),round(maxlaps, 1),str(trackConfiguration)))

    if fuelpercent < 10:
        ac.setFontColor(label1, *rgb(colors["red"], 1.0))
    elif fuelpercent >= 10 and fuelpercent < 30:
        ac.setFontColor(label1, *rgb(colors["orange1"], 1.0))
    elif fuelpercent >= 30 and fuelpercent < 50:
        ac.setFontColor(label1, *rgb(colors["orange2"], 1.0))
    elif fuelpercent >= 50 and fuelpercent < 70:
        ac.setFontColor(label1, *rgb(colors["yellow"], 1.0))
    else:
        ac.setFontColor(label1, *rgb(colors["white"], 1.0))


# aux methods
def rgb(color, a=1, bg=False):
    r = color[0] / 255
    g = color[1] / 255
    b = color[2] / 255
    if bg == False:
        return r, g, b, a
    else:
        return r, g, b
