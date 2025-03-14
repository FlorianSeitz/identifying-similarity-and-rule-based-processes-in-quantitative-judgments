from expyriment import control, design, stimuli, misc, io


class Display(libscreen.Display): 
    def __init__(self, pygamewindow):
        expdisplay = window
        self.dispsize = window.get_size() 
        self.fgc = (0, 0, 0)
        self.bgc = (128, 128, 128)
        self.mousevis = False
disp = Display(window)

def calibrator(tracker, message_1 = u'Es geht nun weiter mit dem Experiment, bitte legen Sie sich die Tastatur zurecht.', message_2 = u'Bitte beachten Sie, dass Sie zwischen den Durchg�ngen auf das Fixationskreuz', message_3 = u'schauen m�ssen, da es andernfalls nicht weitergeht!'):
    if (tracker.recording):
        rrrecorder = True
        while (tracker.recording):
            tracker.stop_recording()
            exp.clock.wait(10)
    else:
        rrrecorder = False
    window = exp.screen._surface # Get current surface
    instro = stimuli.BlankScreen()
    stimuli.TextLine(u'Kalibrierung notwendig.', position = (0, 100), text_size = 40, text_bold = False).plot(instro)
    stimuli.TextLine(u'Sie werden in der Mitte des Bildschirms einen pulsierenden Kreis sehen.', position = (0, 50), text_size = 25, text_bold = False).plot(instro)
    stimuli.TextLine(u'Fokussieren Sie bitte den Kreis und bet�tigen danach die Leertaste um zu beginnen.', position = (0, 0), text_size = 25, text_bold = False).plot(instro)
    stimuli.TextLine(u'Der Kreis wird sich daraufhin anfangen �ber den Bildschirm zu bewegen.', position = (0, -50), text_size = 25, text_bold = False).plot(instro)
    stimuli.TextLine(u'Folgen Sie ihm bitte mit dem Blick.', position = (0, -100), text_size = 25, text_bold = False).plot(instro)
    stimuli.TextLine(u'Sobald die Kalibrierung abgeschlossen ist, geht es weiter mit dem Experiment.', position = (0, -150), text_size = 25, text_bold = False).plot(instro)
    stimuli.TextLine(u'Mit "Leertaste" weiter', position = (0, 50 - exp.screen.size[1]/2), text_size = 25, text_bold = False).plot(instro)
    instro.present(clear = False)
    instro.present(clear = False) # Show calibration screen
    exp.keyboard.wait(misc.constants.K_SPACE) # Wait for space
    pygame.display.set_mode((1680, 1050)) # Enable windowed mode (clears screen content)
    tracker.calibrate() # Run calibration
    pygame.display.set_mode((1680, 1050), pygame.DOUBLEBUF | pygame.FULLSCREEN) # Enable fullscreen again
    disp = Display(window) # Restore eye tracker window
    tracker = eyetracker.EyeTracker(disp, logfile="log/%d" % exp.subject) # Restore eye tracker
    #between_blocks(message_1, message_2, message_3)
    fixcross.present(clear = True)
    fixcross.present(clear = True) # Show fixcross again
    if (rrrecorder):
        while not (tracker.recording):
            tracker.start_recording()
            exp.clock.wait(10)
    return

def gaze_awaiter(tracker):
    fixcross_waiter = libgazecon.AOI('circle', (exp.screen.size[0]/2,exp.screen.size[1]/2), 200)
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
            tracker.log("recalibrating")
            calibrator(tracker)
            breaker = 0
            pass
        pass
    return True

def trial(optionz, typ, block, trial_number):
    tracker.log("starting recording")
    iViewXAPI.iV_SendImageMessage("starting recording")
    try:
        tracker.start_recording()
        tracker.log("recording started")
        iViewXAPI.iV_SendImageMessage("recording started")
    except:
        tracker.log("already recording")
        iViewXAPI.iV_SendImageMessage("already recording")
        pass
    tracker.log("block %d, trial %d" % (block, trial_number))
    iViewXAPI.iV_SendImageMessage("block %d, trial %d"  % (block, trial_number))
    
    #background.preload(inhibit_ogl_compress = True) ## wenn man preloaded, muss man open gl ausschalten (sonst funktioniert der hack von oben nicht)
    
    tracker.log("fixation-screen")
    iViewXAPI.iV_SendImageMessage("fixation-screen")
    gaze_awaiter(tracker)
    #exp.clock.wait(iti)
    tracker.log("trial starts")
    iViewXAPI.iV_SendImageMessage("trial starts")
    
    tracker.log("frames appear")
    iViewXAPI.iV_SendImageMessage("frames appear")
    background.present(clear = False)
    background.present(clear = False)
    key, rt = exp.keyboard.wait()
    tracker.log("response given")
    iViewXAPI.iV_SendImageMessage("response given")
    
    tracker.log("stopping recording")
    iViewXAPI.iV_SendImageMessage("stopping recording")
    tracker.stop_recording()
    tracker.log("recording stopped")
    iViewXAPI.iV_SendImageMessage("recording stopped")
    exp.data.save()
    pass


