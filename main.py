def obey(action):
    basic.show_string(action)

def decode(this):
    if this == '---':
        return 'S'
    elif  this == '...':
        return 'O'
    else:
        return ' '
      
def morse_check():
    global DASH, LETTER, LOUD, QUIET  
    global listening, beeping
    letter = ' '
    pattern = ""
    if listening:
        if beeping: 
            # if input.sound_level() < QUIET:
            if not input.button_is_pressed(Button.A):
                beepOff = control.millis()
                beeping = False 
                # analyse length of beep that just stopped
                length = beepOff - beepOn
                if length > DASH:
                    pattern += '-'
                else:
                    pattern += '.'                
            # else just let the beep continue...
        else: # how long since last beep stopped?
            gap = control.millis() - beepOff
            if gap > LETTER:
                listening = False
                letter = decode(pattern)
                pattern = ''
            # else keep listening for more dots or dashes
    else:
        # if input.sound_level() > LOUD:
        if input.button_is_pressed(Button.A):
            beepOn = control.millis()
            listening = True
    return (letter)

def on_forever():
    # do all kinds of stuff...
    basic.show_icon(IconNames.HEART)
    # check for morse command
    command = morse_check()   
    if command != ' ':
        obey(command)

    

DASH = 500
LETTER = 1000
LOUD = 200
QUIET = 100
listening = False
beeping = False
beepOn = 0
beepOff = 0
basic.forever(on_forever)