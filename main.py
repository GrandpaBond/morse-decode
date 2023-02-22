def obey(str: command):
    pass

def decode(str: code):
    pass


    

def morse_check():
    letter = '?'
    pattern = ""
    if listening:
        if beeping: 
            if input.sound_level() < QUIET:
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
        if input.sound_level() > LOUD:
            beepOn = control.millis()
            listening = True
    return (letter)

def on_forever():
    # do all kinds of stuff...
    basic.show_icon(IconNames.HEART)
    # check for morse command
    code = morse_check()   
    if code = "?" :
        pass
    else:
        obey(letter)

    

DASH = 500
LETTER = 1000
LOUD = 200
QUIET = 100
listening = False
beeping = False
beepOn = 0
basic.forever(on_forever)