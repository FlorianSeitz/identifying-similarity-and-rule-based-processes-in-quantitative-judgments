#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 10.04.2017

@author: Rebecca Albrecht (Eyetracking Interface: Mikhail Spektor)
'''

import os
from expyriment import control, design, stimuli, misc, io
from expyriment.design import randomize
import random
import pygame
import numpy
import csv
from copy import deepcopy



### Stuff to change
i0 = "Liebe Versuchsteilnehmerin, lieber Versuchsteilnehmer,\r\n\r\nvielen Dank, dass Sie an unserem Experiment teilnehmen! In diesem Experiment untersuchen wir, welche Strategien Menschen nutzen, um zu einem Urteil zu gelangen. Dazu werden Sie innerhalb dieses Experiments zunächst lernen, den Wert von verschiedenen Stimuli einzuschätzen. Anschließend werden Ihnen neue Stimuli gezeigt, die Sie einschätzen sollen. \r\n\r\nZusätzlich werden wir in diesem Experiment Ihre Blickbewegeungen aufzeichnen."

i1 = "In der Urteilsaufgabe sollen Sie einschätzen, wie viel Kohle eine Gruppe Zwerge für verschiedenen Funde bekommt, die sie aus einem Bergwerk geborgen haben. Jeder Fund besteht aus einer eckigen und einer runden Scheibe. Die beiden Scheiben haben jeweils zwischen 1 und 4 Einkerbungen. Im Falle der eckigen Scheibe sind die Einkärbungen rund, im Falle der Runden Scheibe sind die Einkärbungen rechteckig. In der Mitte des Bildschirms sehen Sie einen Fund, wie er im Experiment vorkommen kann. Wie viel Kohle die Zwerge für die Scheiben bekommen, hängt von der Beschaffenheit der Funde und der Anzahl der Einkerbungen in den beiden Scheiben ab.\r\n\r\nIn diesem Beispiel sind auf beiden Scheiben vier Einkerbungen sichtbar. Die Zwerge halten den Fund für sehr wertvoll. Klicken Sie auf die linke Maustaste um ein weiteres Beispiel zu sehen."

i2 = "In diesem Beispiel ist jeweils nur eine Einkerbung auf den beiden Scheiben sichtbar, die Zwerge sind mit diesem Fund nicht sehr zufrieden.\r\n\r\nIhre Aufgabe wird es sein zu lernen, wie viel Kohle die Zwerge für verschiedene Funde bekommen."

i3 = "Das Experiment teilt sich in vier verschiedene Phasen auf. In der ersten Phase geht es um einen Wahrnehmungstest. In der zweiten Phase lernen Sie vier Beispielfunde kennen. In der dritten Phase lernen Sie anhand der Beispielsfunden wie viel Kohle verschiedene Funde wert sind. In der vierten Phase sollen Sie anhand Ihres gelernten Wissens den Wert von weiteren Funden einschätzen. Ganz am Ende bitten wir Sie uns kurz ein paar Fragen zu den gelernten Funden und ihrer Person zu beantworten.\r\n\r\nIn der jetzt folgenden ersten Phase sehen Sie jeweils für kurze Zeit einen Fund in der Mitte des Bildschirms. Nachdem der Fund ausgeblendet wurde, erscheinen vier verschiedene Funde in den vier Ecken des Bildschirms. Wir bitten Sie, den Fund auszuwählen, den Sie für eine kurze Zeit in der Mitte gesehen haben. Sie können einen Fund auswählen, indem sie mit der Maus auf den jeweiligen Fund klicken. Bitte klicken Sie auf die linke Maustaste, um mit der ersten Phase zu beginnen. "

i6 = "In diesem Experiment zeichnen wir zusätzlich zu Ihren Antworten Ihre Blickbewegungen auf. Im nächsten Bildschirm wird hierzu eine Kalibrierung des Eyetrackers vorgenommen. Zwischen den einzelnen Aufgaben wird überprüft, ob der Eyetracker noch korrekt kalibriert ist. Hierzu bitten wir Sie, nach jeder Aufgabe auf das Fixationskreuz in der Mitte des Bildschirms zu schauen. Nur wenn Sie das Kreuz fixieren, geht es weiter zur nächsten Aufgabe. Sollte der Eyetracker Ihre Fixation nicht dem Fixationskreuz zuordnen können, wird eine neue Kalibrierung gestartet.\r\n\r\n"

iPhase2 = "Sie haben die erste Phase des Experiments abgeschlossen!\r\n\r\n In der jetzt folgenden zweiten Phase, sollen Sie sich mit vier Beispielsfunden vertraut machen, die auch im weiteren Verlauf des Experiments wichtig sind. Jeder Beispielsfund ist einer der Ecken des Bildschirms zugeordnet und wird auch immer an derselben Stelle gezeigt.\r\n\r\n In jedem Durchgang sehen Sie einen Fund in der Mitte und müssen entscheiden, ob es sich dabei um einen der 4 Beispielsfunde handelt oder nicht. Wenn Sie denken, dass es sich um einen der 4 Beispielsfunde handelt, klicken Sie auf den grauen Kasten in der Ecke, die diesem Fund zugeordnet ist. Wenn Sie denken, dass der gezeigte Fund kein Beispielsfund ist, klicken Sie auf den ‚Unbekannt‘-Button in der unteren Bildschirmhälfte.\r\n\r\nAm Anfang und in regelmäßigen Abständen während dieser Phase werden Ihnen alle vier Beispielsfunde an den jeweils zugeordneten Position angezeigt. Hier können Sie sich so viel Zeit lassen wie Sie möchten, um sich die Beispielsfunde und ihre Positionen gut einprägen."

iPhase3 = "Sie haben die zweite Phase des Experiments abgeschlossen!\r\n\r\n In der jetzt folgenden dritten Phase, sollen Sie lernen wie viel Kohle vier verschiedene Beispielfunde aus der zweiten Phase wert sind. Jeder Fund ist immer noch der selben Ecken des Bildschirms zugeordnet und wird auch immer an dieser Stelle gezeigt.\r\n\r\n In jedem Durchgang sehen Sie einen Fund und müssen entscheiden wie viel Kohle er wert ist. Wenn Sie sich eine Antwort überlegt haben, klicken Sie bitte auf die linke Maustaste. Es erscheint dann eine Skala mit Werten zwischen 1 und 30 auf der Sie Ihre Antwort durch anklicken des entsprechenden Werts angeben können. Danach erhalten Sie Feedback, ob Ihre Einschätzung des Werts korrekt war und der Fund wird wieder eingeblendet.\r\n\r\n Bitte beachten Sie: (1) Für die Eingabe Ihrer Schätzung auf der Skala haben Sie nur zwei Sekunden Zeit. Bitte überlegen Sie sich daher zunächst Ihre Antwort und geben Sie diese anschließend direkt auf der Skala ein. \r\n\r\n(2) Es ist sehr wichtig, dass Sie sich den Fund jeweils genau einprägen und nicht nur die jeweilige Ecke, in der der Fund präsentiert wird! In der vierten Phase müssen Sie Ihr Wissen über die Funde nutzen, um neue Funde einzuschätzen. Dabei ist es wichtig, dass Sie die Funde so gut wie möglich einschätzen. Merken Sie sich daher den Fund jeweils genau!"

iPhase4 = "Sie haben die dritte Phase des Experiments abgeschlossen!\r\n\r\nIn der nächsten und letzten Phase des Experiments zeigen wir Ihnen verschiedene Funde in der Mitte des Bildschirms. Der Fund, den Sie einschätzen sollen, wird nur für kurze Zeit eingeblendet und dann wieder ausgeblendet. Deswegen ist es wichtig, dass Sie sich auf den Fund konzentrieren. Nachdem der Fund wieder ausgeblendet wurde, haben Sie so viel Zeit wie sie möchten, um zu entscheiden wie viel der Fund Wert ist. Wenn Sie sich Ihre Antwort überlegt haben, klicken Sie bitte auf die linke Maustaste, um Ihre Antwort auf der Skala einzugeben. Denken Sie daran, dass Sie weiterhin nur 2 Sekunden haben, um Ihre Antwort einzugeben. Klicken Sie also erst auf die linke Maustaste, wenn Sie sich ihrer Antwort sicher sind. \r\n\r\n In dieser Phase bekommen Sie kein Feedback mehr darüber, ob Ihre Antwort richtig war. Trotzdem ist es wichtig, dass Sie die Funde so gut wie möglich einschätzen." 

iPhase5 = "Das Experiment ist jetzt beinahe beendet! Als letztes bitten wir Sie, noch einen Gedächtnistest durchzuführen. Dazu sehen Sie immer einen Fund und müssen entscheiden, ob dieser Fund einer der Funde aus der Trainingsphase war und in welcher Ecke er präsentiert wurde. Wenn Sie denken, dass der gezeigte Fund einer der vier Funde, die Sie im Training gelernt haben, war, klicken Sie auf die Position, an welcher er immer präsentiert wurden. Wenn Sie denken, dass Sie den gezeigten Fund nicht aus der Trainingsphase kennen, klicken Sie auf den 'Unbekannt'-Button um zu signalieren, dass des Funds nicht aus der Trainingsphase bekannt ist. Danach ist das Experiment beendet." 

iDone = "Das Experiment ist jetzt beendet. Vielen Dank, dass Sie teilgenommen haben!"

# Proceed with key or after a certain amount of time
bool_clock = False
debug=False

## Init
control.defaults.open_gl=0
control.set_develop_mode(debug)
control.defaults.window_size = (1400,700)
exp = design.Experiment() 
ctrl=control.initialize(exp)
ctrl.mouse.show_cursor()

pal = [pygame.Color("#4c8532"), pygame.Color("#2b4f1b"), pygame.Color("#ba40cc"), pygame.Color("#71237d")]

test_scale_time=1000

#Globals
screen_x = exp.screen.size[0]
screen_y = exp.screen.size[1]
window = exp.screen._surface
writer = 0
block_num = 0
validation_size = 250


psych_blocks = 5
memory_blocks = 15
memory_correct = 3
training_blocks = 10
training_correct = 3
test_blocks = 8


background = stimuli.BlankScreen(colour=misc.constants.C_WHITE)

### Start of the eyetracking stuff

dist_factor = -35
offset_x = dist_factor*1.841#screen_x/distance_to_edge_factor_x
offset_y = dist_factor#screen_y/distance_to_edge_factor_y

aoi_size_factor = 6 #The higher the smaller
aoi_size_x = screen_x/aoi_size_factor
aoi_size_y = screen_y/aoi_size_factor

pos_upper_left = (-screen_x/4-offset_x, screen_y/4+offset_y)
pos_upper_right = (screen_x/4+offset_x,screen_y/4+offset_y)
pos_lower_left = (-screen_x/4-offset_x,-screen_y/4-offset_y)
pos_lower_right = (screen_x/4+offset_x,-screen_y/4-offset_y)
pos_mid = (0,0)


aoi_ll = stimuli.Rectangle((aoi_size_x,aoi_size_y), misc.constants.C_GREY, position=(pos_lower_left))
aoi_lr = stimuli.Rectangle((aoi_size_x, aoi_size_y), misc.constants.C_GREY, position=(pos_lower_right))
aoi_ul = stimuli.Rectangle((aoi_size_x, aoi_size_y), misc.constants.C_GREY, position=(pos_upper_left))
aoi_ur = stimuli.Rectangle((aoi_size_x, aoi_size_y), misc.constants.C_GREY, position=(pos_upper_right))
aoi_m = stimuli.Rectangle((aoi_size_x, aoi_size_y), misc.constants.C_GREY, position=pos_mid)
aoi_ll.preload()
aoi_lr.preload()
aoi_ul.preload()
aoi_ur.preload()
aoi_m.preload()



bool_plot_aoi=True
bool_plot_aoi_mid = True

color_1_1 = misc.constants.C_BLUE
color_1_2 = misc.constants.C_EXPYRIMENT_PURPLE
color_2_1 = misc.constants.C_RED
color_2_2 = misc.constants.C_EXPYRIMENT_ORANGE 

cue_value_dist=(aoi_size_x+aoi_size_y)/28#(aoi_size_x+aoi_size_y)/16
radius_max = (aoi_size_x+aoi_size_y)/7
cue_value_dist_square=(aoi_size_x+aoi_size_y)/16
square_size_max = (aoi_size_x+aoi_size_y)/4

offset_adjustment = 0#(aoi_size_x+aoi_size_y)/80
aoi_size_y/2-radius_max

text_size_default = 25
text_color_default = misc.constants.C_BLACK

fixcross = stimuli.FixCross()
fixcross.preload()

### Step procedure: https://www.sciencedirect.com/science/article/pii/S0042698997003404?via%3Dihub
step_size_up = 400 # Between sigma/2 and sigma, where sigma is variance in psychometric function
step_size_down = step_size_up*0.8415

# 4down/1up with ratio up/down .8415 yields 85% correctness
steps_up = 1
steps_down = 4
steps_down_counter = 0

time = 4000
time_vec = []
current_dir = -1
time_test = 1500

num_reversals = 12
bool_psych_done = False

time=2000

response_keys = [misc.constants.K_z, misc.constants.K_n]

score = 0
score_factor=0.0005

writer = 0

s_vec = [pos_upper_left, pos_upper_right, pos_lower_left, pos_lower_right]         
#random.shuffle(s_vec)
cue_pos_vec=range(2)
random.shuffle(cue_pos_vec)
#cue_pos_vec=[1,0]


try:
    # Eyetracker stuff
    import pygaze
    from pygaze import eyetracker
    from pygaze._eyetracker.iViewXAPI import iViewXAPI
    from pygaze import libgazecon
    from pygaze import libscreen

    class Display(libscreen.Display): 
        def __init__(self, pygamewindow):
            pygaze.expdisplay = window
            self.dispsize = window.get_size() 
            self.fgc = (0, 0, 0)
            self.bgc = (128, 128, 128)
            self.mousevis = False
    disp = Display(window)
except:
    debug = True
    pass

    
def send_to_log(m):
    print(m)
    if not debug:
        tracker.log(m)
        iViewXAPI.iV_SendImageMessage(m)

def stop_recording_and_save(m):
    if not debug:
        tracker.stop_recording()
        send_to_log(m)
        exp.data.save()        
        
def calibrator(tracker, text = 2):
    if (tracker.recording):
        rrrecorder = True
        while (tracker.recording):
            tracker.stop_recording()
            exp.clock.wait(10)
    else:
        rrrecorder = False
    window = exp.screen._surface # Get current surface
    instro = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    if text==1:
        stimuli.TextBox(u'Als Erstes findet nun eine Kalibrierung des Eyetrackers statt.\r\nFokusieren Sie bitte den Kreis und sagen Sie dann dem Versuchsleiter Bescheid. Der Kreis wird daraufhin anfangen sich über den Bildschirm zu bewegen. Folgen Sie ihm bitte mit dem Blick. Sobald die Kalibrierung abgeschlossen ist, geht es los mit dem Experiment.\r\n\r\nZwischen den einzelnen Aufgaben wird immer wieder überprüft, ob der Eyetracker noch richtig eingestellt ist. Hierzu bitten wir Sie zwischen den Aufgaben immer wieder auf das Fixationskreuz in der Mitte zu schauen. Sollte der Eyetracker das nicht richtig erkennen, wird die Kalibrierung wiederholt.', position=(0,-screen_y/4), size=(screen_x-(screen_x*.1), screen_y-(screen_y*.2)), text_size = text_size_default, text_colour = text_color_default).plot(instro)
        message_1 = u'Das Experiment geht jetzt los.\r\n\r\nBitte beachten Sie, dass Sie zwischen den Durchgängen auf das Fixationskreuz schauen müssen, da es andernfalls nicht weitergeht!'
    else:
        stimuli.TextBox(u'Kalibrierung notwendig:\r\nSie werden in der Mitte des Bildschirms einen pulsierenden Kreis sehen. \r\nFokusieren Sie bitte den Kreis und sagen Sie dann dem Versuchleiter Bescheid. Der Kreis wird daraufhin anfangen sich über den Bildschirm zu bewegen. Folgen Sie ihm bitte mit dem Blick. Sobald die Kalibrierung abgeschlossen ist, geht es weiter mit dem Experiment.', position=(0,-screen_y/4), size=(screen_x-(screen_x*.1), screen_y-(screen_y*.2)), text_size = text_size_default, text_colour = text_color_default).plot(instro)
        message_1 = u'Das Experiment geht jetzt los.\r\n\r\nBitte beachten Sie, dass Sie zwischen den Durchgängen auf das Fixationskreuz schauen müssen, da es andernfalls nicht weitergeht!'
    instro.present(clear = False)
    instro.present(clear = False) # Show calibration screen
    wait_for_next(instro)
    #exp.keyboard.wait() # Wait for space
    pygame.display.set_mode((screen_x, screen_y)) # Enable windowed mode (clears screen content)
    pygame.display.update()
    try:
        res=tracker.calibrate() # Run calibration
        if res:
            pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN) # Enable fullscreen again
            disp = Display(window) # Restore eye tracker window
            tracker = eyetracker.EyeTracker(disp, logfile="log/%d" % exp.subject) # Restore eye tracker
            between_blocks(message_1)
            fixcross.present(clear = True)
            fixcross.present(clear = True) # Show fixcross again
            if (rrrecorder):
                while not (tracker.recording):
                    tracker.start_recording()
                    exp.clock.wait(10)
            return
        else:
            calibrator(tracker)
    except:
        calibrator(tracker)
    
    
def gaze_awaiter(tracker):
    fixcross_waiter = libgazecon.AOI('circle', (screen_x/2,screen_y/2), validation_size)
    waiter = 0
    breaker = 0
    while True:
        if fixcross_waiter.contains(tracker.sample()):
            waiter += 1
            pass
        else:
            waiter = 0
        exp.clock.wait(1)
        if waiter >= 1000:
            break
        breaker += 1
        if breaker >= 12000:
            send_to_log("recalibrating")
            calibrator(tracker)
            breaker = 0
            pass
        pass
    return True

def check_tracker(block, trial_number, cond):
    send_to_log("starting recording")
    try:
        tracker.start_recording()
        send_to_log("recording started")
    except:
        send_to_log("already recording")
        pass
    send_to_log("block %d, trial %d, condition %d" % (block, trial_number, cond))
    
    send_to_log("fixation-screen")
    if not debug:
        gaze_awaiter(tracker)
    send_to_log("calibration ok")
    pass


class Exemplar:
    def __init__(self, name, values, crit, pos, known=-1):
        self.name = name
        self.values = values
        self.crit = crit
        self.pos = pos
        self.known = known

      

def read_csv(file, range_num, cue_num=2, psych=False):
    exemplars = dict()
    i = 0
    pos_i = -1
    pos_vec = range(range_num)
    random.shuffle(pos_vec)
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            r = row[0].split(";")
            name = r[0]
            if(pos_i>-1):
                pos=pos_vec[pos_i]
            pos_i+=1     
            a = (r[1], r[2])
            
            if i>0:
                values = (a[cue_pos_vec[0]], a[cue_pos_vec[1]])
                crit = r[3]
                if psych:
                    known=r[4]
                else:
                    known=-1
                ex = Exemplar(name, values, crit, pos, known)
                exemplars[name]=ex
            i = i+1
    return exemplars




def show_instruction(text,canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE), bool_mid = True):
    if bool_mid:
        instruction = stimuli.TextBox(text.decode('utf-8'), position=(0,-screen_y/3.5), size=(screen_x-(screen_x*.25), screen_y-(screen_y*.2)), text_justification=(1), text_size = text_size_default, text_colour = text_color_default)
    else:
        instruction = stimuli.TextBox(text.decode('utf-8'), position=(0,0), size=(screen_x-(screen_x*.1), screen_y-(screen_y*.2)), text_justification=(1), text_size = text_size_default, text_colour = text_color_default)
    instruction.plot(canvas)
    wait_for_next(canvas)

def instructions():
    show_instruction(i0)
    global bool_plot_aoi
    bool_plot_aoi = False
    global bool_plot_aoi_mid
    bool_plot_aoi_mid = True
    s=Exemplar("44", [4,4], 0, 0)
    canvas=create_canvas(s, True)
    show_instruction(i1,canvas, False)
    
    s=Exemplar("11", [1,1], 0, 0)
    canvas=create_canvas(s, True)
    show_instruction(i2, canvas, False)
   
    canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    aoi_ll.plot(canvas)
    aoi_lr.plot(canvas)
    aoi_ul.plot(canvas)
    aoi_ur.plot(canvas) 
    show_instruction(i3, canvas)
    
    canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    show_instruction(i6, canvas)
    

def create_cue_circle_2(cue_val, reference_point, adjustment, color_1, color_2):
    stim_dict = {}
    for x in range(cue_val):
        col = color_1
        if x == 1:
            size = (cue_value_dist*2.5, cue_value_dist)
            pos = (+square_size_max/2-cue_value_dist*2, 0)
        elif x == 0:
            size = (cue_value_dist*2.5, cue_value_dist)
            pos = (-square_size_max/2+cue_value_dist*2, 0)
        elif x == 2:
            size = (cue_value_dist, cue_value_dist*2.5)
            pos = (0, +square_size_max/2-cue_value_dist*2)
        elif x == 3:
            size = (cue_value_dist, cue_value_dist*2.5)
            pos = (0, -square_size_max/2+cue_value_dist*2)
        stim = stimuli.Rectangle(size, col, position=(tuple(map(lambda(x,y,z):x+y+z, zip(reference_point, adjustment, pos)))))
        stim_dict[x+2]=stim
    for x in range(2):
        if(x % 2)==0:
            col = color_1
        else:
            col = color_2
        stim = stimuli.Circle(radius_max-cue_value_dist*x, col, position=(tuple(map(sum, zip(reference_point, adjustment)))))
        stim_dict[x]=stim
    return stim_dict
        

def create_cue_square_2(cue_val, reference_point, adjustment, color_1, color_2):
    stim_dict = {}
    for x in range(cue_val):
        col = color_1
        radius=cue_value_dist/1.1
        factor=2.5
        if x == 0:
            #size = (cue_value_dist*2.5, cue_value_dist)
            pos = (+square_size_max/2-cue_value_dist*factor, -square_size_max/2+cue_value_dist*factor)
            #pos=(0,0)
        elif x == 1:
            #size = (cue_value_dist*2.5, cue_value_dist)
            pos = (-square_size_max/2+cue_value_dist*factor, +square_size_max/2-cue_value_dist*factor)
        elif x == 2:
            #size = (cue_value_dist, cue_value_dist*2.5)
            pos = (-square_size_max/2+cue_value_dist*factor, -square_size_max/2+cue_value_dist*factor)
            
        elif x == 3:
            #size = (cue_value_dist, cue_value_dist*2.5)
            pos = (+square_size_max/2-cue_value_dist*factor, +square_size_max/2-cue_value_dist*factor)
            #pos=(0,0)
        stim = stimuli.Circle(radius, col, position=(tuple(map(lambda(x,y,z):x+y+z, zip(reference_point, adjustment, pos)))))
        stim_dict[x+2]=stim
        
    for x in range(2):
        if(x % 2)==0:
            col = color_1
        else:
            col = color_2
        stim = stimuli.Rectangle((square_size_max-cue_value_dist_square*x, square_size_max-cue_value_dist_square*x) , col, position=(tuple(map(sum, zip(reference_point, adjustment)))))
        stim_dict[x]=stim
    return stim_dict
    
def create_stim(cue_val_1, cue_val_2, pos, canvas):
    pos_x=pos[0]
    pos_y=pos[1]
    #if(pos==(0,0)):
    #    line_col = misc.constants.C_GREY
    #else:
    #    line_col = misc.constants.C_WHITE
    line_col = misc.constants.C_WHITE
    mid_line=stimuli.Line((pos_x, pos_y-aoi_size_y/2), (pos_x, pos_y+aoi_size_y/2), 2, line_col)
    mid_line.plot(canvas)
    if (exp.subject % 2) == 0:
        adjustment_tmp_1 = (aoi_size_x/2-square_size_max/2-offset_adjustment,aoi_size_y/2-square_size_max/2-offset_adjustment)
        adjustment_tmp_2 = (-(aoi_size_x/2-radius_max-offset_adjustment),-(aoi_size_y/2-radius_max-offset_adjustment))
    else:
        adjustment_tmp_1 = (-(aoi_size_x/2-square_size_max/2-offset_adjustment),-(aoi_size_y/2-square_size_max/2-offset_adjustment))
        adjustment_tmp_2 = (aoi_size_x/2-radius_max-offset_adjustment,aoi_size_y/2-radius_max-offset_adjustment)
        
    if (exp.subject % 4) < 2:
        cue_dict_1 = create_cue_square_2(cue_val_1, pos, adjustment_tmp_1, pal[2], misc.constants.C_WHITE)
        cue_dict_2 = create_cue_circle_2(cue_val_2, pos, adjustment_tmp_2, pal[0], misc.constants.C_WHITE)
    else:
        cue_dict_1 = create_cue_square_2(cue_val_1, pos, adjustment_tmp_1, pal[0], misc.constants.C_WHITE)
        cue_dict_2 = create_cue_circle_2(cue_val_2, pos, adjustment_tmp_2, pal[2], misc.constants.C_WHITE)
        
    for x in range(cue_val_1+2):
        cue_dict_1[x].plot(canvas)    
    
    for x in range(cue_val_2+2):
        cue_dict_2[x].plot(canvas)
    return canvas
    
def wait_for_next(canvas, crit=-1, rt=-1, next_bool=True, pos = (0, (-control.defaults.window_size[1]/2+25))):
    #button_next = stimuli.Rectangle(size=(200, 50), colour=misc.constants.C_GREY, line_width=0, position=pos)
    text_next = stimuli.TextLine("Weiter geht es mit einem Klick auf die linke Maustaste.", pos, text_colour = misc.constants.C_BLACK)                                
    if next_bool:
        #button_next.plot(canvas)
        text_next.plot(canvas)                       
    canvas.present()
    id, pos_press, rt = exp.mouse.wait_press()
    return rt
    #if button_next.overlapping_with_position(pos_press):
    #    return crit, rt
    #else:
    #    return wait_for_next(canvas, crit, rt, next_bool, pos)


def create_canvas(s, bool_test):   
    canvas = stimuli.Canvas(colour=misc.constants.C_WHITE, size=(screen_x, screen_y))
    if(bool_plot_aoi):
        aoi_ll.plot(canvas)
        aoi_lr.plot(canvas)
        aoi_ul.plot(canvas)
        aoi_ur.plot(canvas)
    if(bool_plot_aoi_mid):
        aoi_m.plot(canvas)
    
    if s != -1:
        if(bool_test):
            canvas=create_stim(int(s.values[0]), int(s.values[1]), pos_mid, canvas)
        else:
            if isinstance(s, list):
                for elem in s:
                    canvas=create_stim(int(elem.values[0]), int(elem.values[1]), s_vec[elem.pos], canvas)
            else:
                canvas=create_stim(int(s.values[0]), int(s.values[1]), s_vec[s.pos], canvas)
    return canvas
    

def present_canvas(s, b, t, pos=True, fc=True):
    send_to_log("create canvas...")
    if s != -1:
        if not debug and fc:
            fixcross.present(clear = True)
            send_to_log("fixation-screen presented")
            check_tracker(b, t, 0)
        if isinstance(s, list):
            for elem in s:
                send_to_log("item: " + elem.name)
                send_to_log("pos: " + str(elem.pos))
        else:
            send_to_log("item: " + s.name)
            send_to_log("pos: " + str(s.pos))
    canvas=create_canvas(s, pos)
    send_to_log("canvas created")
    canvas.present()
    send_to_log("canvas presented")
    return canvas

def create_canvas_test(s, bool_test):   
    canvas = stimuli.Canvas(colour=misc.constants.C_WHITE, size=(screen_x, screen_y))
    if(bool_plot_aoi):
        aoi_ll.plot(canvas)
        aoi_lr.plot(canvas)
        aoi_ul.plot(canvas)
        aoi_ur.plot(canvas)
    if(bool_plot_aoi_mid):
        aoi_m.plot(canvas)
    
    if s != -1:
        if(bool_test):
            canvas=create_stim(int(s.values[0]), int(s.values[1]), pos_mid, canvas)
        else:
            if isinstance(s, list):
                for elem in s:
                    canvas=create_stim(int(elem.values[0]), int(elem.values[1]), s_vec[elem.pos], canvas)
            else:
                canvas=create_stim(int(s.values[0]), int(s.values[1]), s_vec[s.pos], canvas)
    return canvas

def present_canvas_test(s, b, t, pos=True, fc=True):
    send_to_log("create canvas...")
    if s != -1:
        if not debug and fc:
            fixcross.present(clear = True)
            send_to_log("fixation-screen presented")
            check_tracker(b, t, 0)
        if isinstance(s, list):
            for elem in s:
                send_to_log("item: " + elem.name)
                send_to_log("pos: " + str(elem.pos))
        else:
            send_to_log("item: " + s.name)
            send_to_log("pos: " + str(s.pos))
    canvas=create_canvas(s, pos)
    send_to_log("canvas created")
    canvas.present()
    send_to_log("canvas presented")
    return canvas    
    
def get_score(j, y):
    score = 10-(numpy.power(int(j)-int(y), 2) /7.625)
    if score < 0:
        return 0
    else:
        return score
    

def do_trial_feedback_mouse(s, b, t):
    send_to_log("training_crit: starting trial, block: %s trial: %s" % (str(b), str(t)))
    canvas=present_canvas(s, b, t, False)
    rt=wait_for_next(canvas, next_bool=False)
    send_to_log("training_crit: response indicated, rt: %s, block: %s trial: %s" % (str(rt), str(b), str(t)))
    send_to_log("training_crit: present scale, block: %s trial: %s" % (str(b), str(t)))
    crit, rt, correct=create_scale(s)
    send_to_log("training_crit: response given: response: %s, block: %s trial: %s" % (str(crit), str(b), str(t)))
    send_to_log("training_crit: rt: %s, block: %s trial: %s" % (str(rt), str(b), str(t)))
    stop_recording_and_save("recording stopped")
    return crit, rt, correct

def create_scale(s, fb=True, tp=False):
    send_to_log("scale: create ...")
    canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    w=35
    boxes=map(lambda(x): stimuli.Rectangle((w,w), position=(x*(w+1)-15*w, 0)), range(30))
    names=map(lambda(x): stimuli.TextLine(str(x+1), position=(x*(w+1)-15*w, 0), text_colour= misc.constants.C_BLACK, text_size=20), range(30))
    for b in boxes:
        b.plot(canvas)
    for n in names:
        n.plot(canvas)
    correct = False
    canvas.present()
    send_to_log("scale: presented")
    max_time = 2000
    id, pos, rt = exp.mouse.wait_press(duration=max_time)
    crit=-1
    send_to_log("scale: response correct: " + str(s.crit))
    if rt == None:
        canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        text = stimuli.TextLine("Das war leider zu langsam. Bitte antworten Sie in der vorgegebenen Zeit von 2 Sekunden!", text_colour=misc.constants.C_BLACK, text_size=20)
        text.plot(canvas)
        canvas.present()
        send_to_log("scale: response too slow, rt: " + str(max_time))
        wait_for_next(canvas)
        return -1,-1, False
    else:
        if fb:
            global bool_plot_aoi
            aoi_ll.plot(canvas)
            aoi_lr.plot(canvas)
            aoi_ul.plot(canvas)
            aoi_ur.plot(canvas)
            canvas=create_stim(int(s.values[0]), int(s.values[1]), s_vec[s.pos], canvas)   
        for i in range(30):
            if boxes[i].overlapping_with_position(pos):
                crit = i+1
                if fb:
                    if crit == int(s.crit):
                        feedback = stimuli.TextBox(("Ihre Antwort " +  str(crit) + " war richtig!").decode('utf-8'), position=(0, -200), size=(screen_x/2, screen_y/4), text_size = text_size_default, text_colour = text_color_default)
                        send_to_log("scale: feedback given")
                        boxes[i].size = (50, 50)
                        boxes[i].colour = misc.constants.C_GREEN
                        boxes[i].plot(canvas)
                        names[i].text_size=25
                        names[i].plot(canvas)
                        correct = True
                    else:
                        feedback = stimuli.TextBox(("Ihre Antwort " +  str(crit) + " war leider falsch.\r\nDie richtige Antwort ist: " + str(s.crit)), position=(0, -200), size=(screen_x/2, screen_y/4), text_size = text_size_default, text_colour = text_color_default)
                        send_to_log("scale: feedback given")
                        boxes[i].size = (50, 50)
                        boxes[i].colour = misc.constants.C_RED
                        boxes[i].plot(canvas)
                        names[i].text_size=25
                        names[i].plot(canvas)
                        real_crit = int(s.crit)
                        boxes[real_crit-1].size = (50, 50)
                        boxes[real_crit-1].colour = misc.constants.C_GREEN
                        boxes[real_crit-1].plot(canvas)
                        names[real_crit-1].text_size=25
                        names[real_crit-1].plot(canvas)
                        correct = False
                    
                else:
                    feedback = stimuli.TextBox("Ihre Antwort ist:" +  str(crit), position=(0, -200), size=(screen_x/2, screen_y/4), text_size = text_size_default, text_colour = text_color_default)    
                    send_to_log("scale: no feedback given")
                    boxes[i].size = (50, 50)
                    boxes[i].colour = misc.constants.C_GREY
                    boxes[i].plot(canvas)
                    names[i].text_size=25
                    names[i].plot(canvas)
                    correct=False
                feedback.plot(canvas) 
                canvas.present()
                wait_for_next(canvas)
                send_to_log("scale: response given, response:" + str(crit))
                send_to_log("scale: response is correct? " + str(correct))
                return crit, rt, correct
    return create_scale(s, fb)
        
                
   
def do_trial_test(s, b, t):
    send_to_log("test_crit: starting trial, block: %s trial: %s" % (str(b), str(t)))
    global bool_plot_aoi_mid
    bool_plot_aoi_mid = True
    send_to_log("test_crit: present target in mid position, block: %s trial: %s" % (str(b), str(t)))
    canvas=present_canvas(s, b, t)
    #canvas_tmp = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    aoi_m_cover = stimuli.Rectangle((aoi_size_x+5, aoi_size_y+5), misc.constants.C_WHITE, position=pos_mid)
    aoi_m_cover.plot(canvas)
    exp.keyboard.wait(keys=response_keys, duration=time_test)
    canvas.present()
    send_to_log("test_crit: remove target from mid position, rt: %s, block: %s trial: %s" % (str(time_test), str(b), str(t)))
    rt = wait_for_next(canvas, next_bool=False)
    send_to_log("test_crit: response indicated, rt: %s, block: %s trial: %s" % (str(rt), str(b), str(t)))
    send_to_log("test_crit: present scale, block: %s trial: %s" % (str(b), str(t)))
    crit, rt, correct=create_scale(s, fb=False)
    send_to_log("test_crit: response given, response: %s, block: %s trial: %s" % (str(crit), str(b), str(t)))
    send_to_log("test_crit: rt: %s, block: %s trial: %s" % (str(rt), str(b), str(t)))
    stop_recording_and_save("recording stopped")
    return crit, rt

def analyse_response(pos):
    if aoi_ul.overlapping_with_position(pos):
        return 0
    elif aoi_ur.overlapping_with_position(pos):
        return 1
    elif aoi_ll.overlapping_with_position(pos):
        return 2
    elif aoi_lr.overlapping_with_position(pos):
        return 3
    else: 
        return -1


def do_trial_psych_new(s, d, b, t, jump=False, plot_aoi_mid= False):
    send_to_log("training_psych: starting trial, block: %s trial: %s" % (str(b), str(t)))
    #canvas = present_canvas_full(s, d, b, t, False)
    global bool_plot_aoi_mid
    bool_plot_aoi_mid = plot_aoi_mid
    if s==-1:
        send_to_log("memory: show all items, block: %s trial: %s" % (str(b), str(t)))
        canvas = present_canvas(d, b, t, False)
        wait_for_next(canvas)
        stop_recording_and_save("recording stopped")
        pass
    else:
        if not jump:
            canvas = present_canvas(s, b, t, True)
            send_to_log("training_psych: show target in mid position, block: %s trial: %s" % (str(b), str(t)))
            global time
            global score
            global current_dir
            global time_vec
            global bool_psych_done
            rt=-1
            aoi_m_cover = stimuli.Rectangle((aoi_size_x+5, aoi_size_y+5), misc.constants.C_WHITE, position=pos_mid)
            aoi_m_cover.plot(canvas)
            exp.keyboard.wait(keys=response_keys, duration=time)
            canvas.present()
            send_to_log("training_psych: remove target from mid position real, rt: %s, block: %s trial: %s" % (str(time_test), str(b), str(t)))
            text="Bitte wählen sie jetzt den Fund, den Sie gerade gesehen habe, aus!".decode('utf-8')
            pos=(0,-screen_y/2)
        else:
            text="Bitte klicken Sie auf den grauen Kasten, in dem der korrekte Fund angezeigt wird.".decode('utf-8')
            pos=(0,-screen_y/2)
        
        bool_plot_aoi_mid = False
        canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        canvas = present_canvas(d, b, t, False, fc=False)
        send_to_log("training_psych: remove target from mid position, rt: %s, block: %s trial: %s" % (str(time), str(b), str(t)))
        timesup = stimuli.TextBox(text, position=pos, size=(screen_x, screen_y), text_size = text_size_default, text_colour = text_color_default)
        timesup.plot(canvas)
        canvas.present()
        send_to_log("training_psych: show target and distractors, block: %s trial: %s" % (str(b), str(t)))
        id, pos, rt = exp.mouse.wait_press()
        real_pos = analyse_response(pos)
        send_to_log("training_psych: response given, response: " + str(real_pos))
        if real_pos == -1:
            send_to_log("training_psych: repeat response because of wrong click")
            return do_trial_psych_new(s, d, b, t, True, plot_aoi_mid= plot_aoi_mid)
        else:
            global steps_down_counter
            if real_pos == s.pos:
                steps_down_counter += 1
                text="Das war richtig!"
                send_to_log("training_psych: psychophysics correct, time: " + str(time))
                if len(time_vec) == 0:
                    steps_down_counter = steps_down
                if steps_down_counter == steps_down:
                    steps_down_counter = 0
                    send_to_log("training_psych: psychophysics correct, old time: " + str(time))
                    time -=step_size_down
                    send_to_log("training_psych: psychophysics correct, new time: " + str(time))
                    add_time = time
                    if(time) < 0:
                        add_time = 0
                    time_vec.append(add_time)
                    current_dir = -1
            else:
                old_time = time
                time +=step_size_up
                text="Das war leider falsch."
                send_to_log("training_psych: psychophysics incorrect, time: " + str(time))
                if current_dir == -1:
                    #time_vec.append(old_time)
                    time_vec.append(time)
                    current_dir = 1
            
            if len(time_vec) >= num_reversals:
                bool_psych_done = True
            
            
            canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
            feedback = stimuli.TextBox(text, position=(0,-screen_y/2), size=(screen_x, screen_y), text_size = text_size_default, text_colour = text_color_default)
            feedback.plot(canvas)
            send_to_log("feedback given")
            wait_for_next(canvas)
            stop_recording_and_save("recording stopped")
            return real_pos, rt, time

def do_trial_mem_test(s, d, b, t, bool_distractor, feedback, jump=False):
    send_to_log("training_memory: starting trial, block: %s trial: %s" % (str(b), str(t)))
    #canvas = present_canvas_full(s, d, b, t, False)
    if(not jump):
        canvas = present_canvas(s, b, t, True)
        text="Weisen Sie dem in der Mitte gezeigten Fund die richtige Position zu. Falls der Fund keine richtige Position hat, drücken Sie den 'Unbekannt'-Button".decode('utf-8')
    else:
        canvas = present_canvas(s, b, t, True, False)
    
    text="Weisen Sie dem in der Mitte gezeigten Fund die richtige Position zu. Falls der Fund keine richtige Position hat, drücken Sie den 'Unbekannt'-Button".decode('utf-8')
    stim = stimuli.TextBox(text, position=(0,-screen_y+150), size=(screen_x, screen_y), text_size = text_size_default, text_colour = text_color_default)
    stim.plot(canvas)
    
    button = stimuli.Rectangle(size=(200, 50), colour=misc.constants.C_GREY, line_width=0, position=(0, -screen_y/4))
    button_text = stimuli.TextLine("Unbekannt", button.position, text_colour = misc.constants.C_WHITE)
    button.plot(canvas)
    button_text.plot(canvas)
    canvas.present()
    send_to_log("training_memory: show item in mid position, block %s trial %s" % (str(b), str(t)))
    id, pos, rt = exp.mouse.wait_press()
    if(button.overlapping_with_position(pos) and bool_distractor):
        text= "Das war richtig!"
        real_pos = "unknown"
        correct_pos = "unknown"
        correct =True
    elif(button.overlapping_with_position(pos) and not bool_distractor):
        text= "Das war leider falsch."
        real_pos = "unknown"
        correct_pos = s.pos
        correct =False
    else:
        real_pos = analyse_response(pos)
        if real_pos == -1:
            send_to_log("training_memory: repeat response because of wrong click, block %s trial %s" % (str(b), str(t)))
            return do_trial_mem_test(s, d, b, t, bool_distractor, feedback, jump=True)
        else:
            if real_pos == s.pos:
                text= "Das war richtig!"
                correct_pos = s.pos
                correct =True
            else:
                text= "Das war leider falsch."
                correct_pos = s.pos
                correct =False
    send_to_log("training_memory: response given, response: %s, block %s trial %s " % (str(real_pos), str(b), str(t)))
    send_to_log("training_memory: response correct: %s, block %s trial %s " % (str(correct_pos), str(b), str(t)))
    send_to_log("training_memory: response is correct? %s, block %s trial %s " % (str(correct), str(b), str(t)))
    canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    if(feedback):
        stim = stimuli.TextBox(text, position=(0,-screen_y/2), size=(screen_x, screen_y), text_size = text_size_default, text_colour = text_color_default)
        stim.plot(canvas)
    else:
        stim = stimuli.TextBox("Klicken Sie auf die linke Maustaste um den nächsten Fund zu sehen.".decode('utf-8'), position=(0,-screen_y/2), size=(screen_x, screen_y), text_size = text_size_default, text_colour = text_color_default)
        stim.plot(canvas)
    canvas.present()
    send_to_log("training_memory: feedback given, block %s trial %s " % (str(b), str(t)))
    wait_for_next(canvas)
    stop_recording_and_save("recording stopped")
    return real_pos, rt, correct

        
def show_all_training_items(training_dict, block=-1):
    training = training_dict.values()
    global bool_plot_aoi
    global bool_plot_aoi_mid
    bool_plot_aoi_mid = False
    bool_plot_aoi = True
    send_to_log("memory: present screen with all training items")
    do_trial_psych_new(-1, training, block, -1, False, False)
    bool_plot_aoi_mid = True
    send_to_log("memory: presentation of screen with all training items done")
        
def do_training(training_dict):
    training = training_dict.values()
    global bool_plot_aoi
    global score
    bool_plot_aoi = True
    global bool_plot_aoi_mid
    bool_plot_aoi_mid = False
    global writer
    
    block = 0
    num_correct_blocks = 0
    done = False
    check_tracker = True
    correct_blocks = 0
    
    while not done:
        randomize.shuffle_list(training)
        num_correct_in_block = 0
        trial = 0
        check_tracker = True
        correct_in_block = 0
        for s in training:
            result, rt, correct = do_trial_feedback_mouse(s, block, trial)
            if(correct):
                correct_in_block +=1
            check_tracker = False
            score+=get_score(result, s.crit)
            writer.writerow(str(exp.subject) + ";" + str(trial) + ";" + str(block) + ";" + str(s.name) + ";" + str(s.values[0]) + ";" + str(s.values[1]) + ";" + str(s.crit) +";" + str(s.known) + ";" + str(result) + ";" + str(rt) + ";" + "0" + ";" + "training" + ";" + "0")
            if result == int(s.crit):
                num_correct_in_block = num_correct_in_block + 1
            trial +=  1
        if num_correct_in_block == len(training):
            num_correct_blocks += 1
            if num_correct_blocks >=3:
                done = True
        block +=  1
        if block == training_blocks:
            break
        if(correct_in_block == 4):
            correct_blocks +=1
        if(correct_blocks == training_correct):
            break

g_distractors = dict([])

def choose_distractors_2(s, dict_test):
    name = s.name
    print name
    v1=int(list(name)[0])
    v2=int(list(name)[1])
    other_num = [x for x in [1,2,3,4] if x != v1 and x != v2]
    d1_name = str(v1) + str(design.randomize.rand_element(other_num))
    d2_name = str(design.randomize.rand_element(other_num)) + str(v2)
    
    all_names = map(lambda(x): x.name, dict_test.values())
    other_names = [x for x in all_names if (x != s.name and x != d1_name and x != d2_name)]
    d3_name = design.randomize.rand_element(other_names)
    distractors=[d1_name, d2_name, d3_name]
    distractors_exempalars = map(lambda(x): dict_test[x], distractors)
    return distractors_exempalars


def do_training_psych(test_dict):
    global bool_plot_aoi
    global bool_plot_aoi_mid
    bool_plot_aoi=True
    bool_plot_aoi_mid = True
    block = 0
    done = False
    block_rt = 0
    block_time = 0
    rt=0
    test = test_dict.values()
    while not done:
        trial = 0
        randomize.shuffle_list(test)
        for s in test:
            test_tmp = deepcopy(test)
            del test_tmp[trial]
            distractors = choose_distractors_2(s, test_dict)
            distractors = distractors + [s]
            distractors_pos = range(4)
            i=0
            random.shuffle(distractors_pos)
            for t in distractors:
                t.pos = distractors_pos[i]
                i+=1
            do_trial_psych_new(s, distractors, block, trial, plot_aoi_mid=True)
            block_rt += rt
            block_time += time
            result = "TODO"
            writer.writerow(str(exp.subject) + ";" + str(trial) + ";" + str(block) + ";" + str(s.name) + ";" + str(s.values[0]) + ";" + str(s.values[1]) + ";" + str(s.crit) +";" + str(s.known) + ";" + str(result) + ";" + str(rt) + ";" + str(time) + ";" + "psych" + ";" + str(score*score_factor))
            trial = trial + 1
        block += 1
        if bool_psych_done:
            done = True
        if block == psych_blocks:
            done = True
              
    global time_test
    time_test = numpy.mean(time_vec[1:len(time_vec)])
    

def create_break_window(num): 
    canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    text = stimuli.TextLine("Jetzt ist Zeit für eine Pause. Nehmen Sie sich so viel Zeit, wie Sie möchten!".decode('utf-8'), text_colour=misc.constants.C_BLACK, text_size=20)
    text.plot(canvas)
    canvas.present()
    wait_for_next(canvas)

def do_test_judg(test_dict):
    test = test_dict.values()
    global bool_plot_aoi
    global bool_plot_aoi_mid
    global score
    bool_plot_aoi=True
    bool_plot_aoi_mid = True
    block = 0
    while block < test_blocks: 
        randomize.shuffle_list(test)
        trial = 0
        for s in test:
            result, rt = do_trial_test(s, block, trial)
            score += get_score(result, s.crit)
            writer.writerow(str(exp.subject) + ";" + str(trial) + ";" + str(block) + ";" + str(s.name) + ";" + str(s.values[0]) + ";" + str(s.values[1]) + ";" + str(s.crit) +";" + str(s.known) + ";" + str(result) + ";" + str(rt) + ";" + "0" + ";" + "judg" + ";" + str(score*score_factor))
            trial += 1
        block += 1
        if(block % 2 == 0 and block < test_blocks):
            create_break_window(str(58+block*5))
        
        
    
def memory_test(training_dict, test_dict, feedback, blocks):
    training=training_dict.values()
    distractors = map(lambda(x): x.name[::-1] , training)
    distractors_exemplars =  map(lambda(x): test_dict[x], distractors)
    for e in distractors_exemplars:
        e.pos = -1
    print(map(lambda(x): (x.name, x.pos), training))
    print(map(lambda(x): (x.name, x.pos), distractors_exemplars))
    print(map(lambda(x): (x.name, x.pos), test_dict.values()))
    items = training + distractors_exemplars
    global bool_plot_aoi
    global bool_plot_aoi_mid
    bool_plot_aoi=True
    
    trial = 0
    block=0
    correct_blocks = 0
    while True:
        correct_in_block = 0
        if(feedback):
            show_all_training_items(training_dict, block)
        else:
            bool_plot_aoi_mid = True
        random.shuffle(items)
        for s in items:
            bool_distr = s.name == distractors_exemplars[0].name or s.name == distractors_exemplars[1].name or s.name == distractors_exemplars[2].name or s.name == distractors_exemplars[3].name
            result, rt, correct = do_trial_mem_test(s, [], block, trial, bool_distr, feedback)
            if(correct):
                correct_in_block += 1
            writer.writerow(str(exp.subject) + ";" + str(trial) + ";" + str(block) + ";" + str(s.name) + ";" + str(s.values[0]) + ";" + str(s.values[1]) + ";" + str(s.crit) +";" + str(s.known) + ";" + str(result) + ";" + str(rt) + ";" + "0" + ";" + "mem_test" + ";" + str(score*score_factor))
            trial += 1
        #canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        #if score > 0:
        #    iDone_real = iDone + str(round(score*score_factor, 1)) + iDone2
        #else: iDone_real = iDone + "0" + iDone2
        if(correct_in_block == 8):
            correct_blocks +=1
        if(correct_blocks == memory_correct):
            break
        block +=1
        if(block==blocks):
            break

def between_blocks(message):
    canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
    stimuli.TextBox(text=message, position=(0,-screen_y/4), size=(screen_x-(screen_x*.1), screen_y-(screen_y*.2)), text_size = text_size_default, text_colour = text_color_default).plot(canvas)
    canvas.present(clear = True)
    canvas.present(clear = False)
    wait_for_next(canvas)
    pass
    
def create_task_screen():
    with open(str("data/results_" + str(exp.subject) + ".csv"), "wb") as csvfile:
        global writer
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(str("subj_id" + ";" + "trial" + ";" + "block" + ";" + "name" + ";" + "cue1" + ";" + "cue2" + ";" + "crt" + ";" + "known" + ";" + "response" + ";" + "rt" + ";" + "time" + ";" + "cond" + ";" + "Bonus"))        
        
        instructions()
        
        if not debug:
            calibrator(tracker, 1)
        
        exemplars_test = read_csv(os.path.join(os.path.dirname(__file__), 'IO/all_eye.csv'), 17)
        exemplars_training = read_csv(os.path.join(os.path.dirname(__file__), "IO/training_eye.csv"), 4)
        
        #send_to_log("training_psych")
        do_training_psych(exemplars_test)
        
        canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        show_instruction(iPhase2, canvas)    
        
        #send_to_log("training_memory")
        memory_test(exemplars_training, exemplars_test, True, memory_blocks)
        
        canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        show_instruction(iPhase3, canvas)    
        
        send_to_log("training_crit")
        do_training(exemplars_training)
        
        canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        show_instruction(iPhase4, canvas)
        
        send_to_log("test_rit")
        do_test_judg(exemplars_test)
        
        canvas=stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        show_instruction(iPhase5, canvas)
        
        send_to_log("test_memory")
        memory_test(exemplars_training, exemplars_test, False, 1)
        
        
def get_subj_info():
    while True:
        txt_input = io.TextInput("Alter:", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
        age = txt_input.get()
        while True:
            try:
                while int(age) not in range(0,100):
                    txt_input = io.TextInput("Bitte das richtige Alter in Jahren angeben!", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
                    age = txt_input.get()
                break
            except ValueError:
                txt_input = io.TextInput("Bitte das richtige Alter in Jahren angeben!", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
                age = txt_input.get()
    
        txt_input = io.TextInput(u"Geschlecht ('w' für weiblich; 'm' für männlich):", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
        sex = txt_input.get()
        while sex.lower() != "m" and sex.lower() != "w":
            txt_input = io.TextInput(u"Bitte das richtige Geschlecht angeben ('w' für weiblich; 'm' für männlich)!", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
            sex = txt_input.get()
    
        if sex.strip().lower() == "m":
            gender = u"männlich"
        elif sex.strip().lower() == "w":
            gender = "weiblich"
    
        txt_input = io.TextInput("Beruf / Studienfach:", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
        #major = misc.str2unicode(txt_input.get())
        major = txt_input.get()
    
        txt_input = io.TextInput(u"Händigkeit ('r' für rechts; 'l' für links):", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
        hand = txt_input.get()
        while hand.lower() != "r" and hand.lower() != "l":
            txt_input = io.TextInput(u"Bitte Händigkeit angeben ('r' für rechts; 'l' für links):", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
            hand = txt_input.get()
    
        if hand.strip().lower() == "r":
            handedness = "rechts"
        elif hand.strip().lower() == "l":
            handedness = "links"
            pass
        
        txt_input = io.TextInput(u"Haben Sie eine Farbsehschwäche? ('j' für ja; 'n' für nein):", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
        coly = txt_input.get()
        while coly.lower() != "j" and coly.lower() != "n":
            txt_input = io.TextInput(u"Haben Sie eine Farbsehschwäche? ('j' für ja; 'n' für nein):", message_colour=misc.constants.C_BLACK, background_colour=misc.constants.C_WHITE)
            coly = txt_input.get()
            pass
        
        if coly.strip().lower() == "j":
            color_problems = "ja"
        elif coly.strip().lower() == "n":
            color_problems = "nein"
            pass 
        
        correct_check = [
            u"Bitte überprüfen Sie die Eingaben:",
            u"Alter: %s" % str(int(age.strip())),
            u"Geschlecht: %s" % gender,
            u"Beruf / Studienfach: %s" % major.strip(),
            u"Händigkeit: %s" % handedness,
            u"Farbsehschwäche: %s" % color_problems,
            u"Wenn die Angaben stimmen, drücken Sie 'j', andernfalls drücken Sie 'n' um die Fragen zu wiederholen"
        ]
        
        canvas = stimuli.BlankScreen(colour=misc.constants.C_WHITE)
        
        pos_y = numpy.linspace(120, -120, len(correct_check))
        
        for xyz in range(len(correct_check)):
            stimuli.TextLine(correct_check[xyz], position = (0, pos_y[xyz]), text_size = text_size_default, text_colour = text_color_default).plot(canvas)
            pass
        
        canvas.present(clear = True)
        canvas.present(clear = False)
        
        correct, irrelevant_rt = exp.keyboard.wait([misc.constants.K_j, misc.constants.K_n])
        if correct == misc.constants.K_j:
            break


    print("Age: %s" % int(age.strip()))
    print("Sex: %s" % sex.strip().lower())
    print("Major: %s" % major.strip().lower())
    print("Handedness: %s" % hand.strip().lower())
    print("Color Blindness: %s" % coly.strip().lower())
    print("s_vec: %s" % s_vec)
    print("cue_pos_vec: %s" % cue_pos_vec)
    print("Test Time: %s" % time_test)
    print("Time Vec: %s" % time_vec)  

        
def do_experiment():
    send_to_log("starting recording")
    print("Pos Vec:")
    print(s_vec)
    print("Cue Pos Vec:")
    print(cue_pos_vec)
    create_task_screen()    
    print("screen x; " + str(screen_x))
    print("screen y; " + str(screen_y))
    print("window; " + str(window))
    print("size validation cross; " + str(validation_size))
    print("psych blocks; " + str(psych_blocks))
    print("memory blocks; " + str(memory_blocks))
    print("memory blocks correct; " + str(memory_correct))
    print("training blocks; " + str(training_blocks))
    print("training blocks correct; " + str(training_correct))
    print("test blocks; " + str(test_blocks))
    print("Size AOI lower left (ll); " + str(aoi_ll.size))
    print("Pos AOI lower left (ll); " + str(aoi_ll.position))
    print("Size AOI lower right (lr); " + str(aoi_lr.size))
    print("Pos AOI lower right (lr); " + str(aoi_lr.position))
    print("Size AOI upper left (ul); " + str(aoi_ul.size))
    print("Pos AOI upper left (ul); " + str(aoi_ul.position))
    print("Size AOI upper right (ur); " + str(aoi_ur.size))
    print("Pos AOI upper right (ur); " + str(aoi_ur.position))
    print("Size AOI mid (m); " + str(aoi_m.size))
    print("Pos AOI mid (m); " + str(aoi_m.position))
    print("Pos Vec:")
    print(s_vec)
    print("Cue Pos Vec:")
    print(cue_pos_vec)
    get_subj_info()


control.start(exp, skip_ready_screen = True)    
try:
    tracker = eyetracker.EyeTracker(disp, logfile="log/%d" % exp.subject)
except:
    tracker = None
    debug = True
    pass

do_experiment()

try:
    iViewXAPI.iV_SaveData("D:\\Rebecca\\%d.idf" % exp.subject, "%d" % exp.subject, "CXCOM_eye", 1)
    iViewXAPI.iV_Disconnect()
except:
    pass
  
exp.data.save()
control.end()
