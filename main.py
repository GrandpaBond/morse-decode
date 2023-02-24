
DOT_MIN = 200
DASH_MIN = 500
LETTER_PAUSE = 1000
LOUD = 200
QUIET = 100

MORSE_TABLE = [
     87,                               # binary tree of state values:
    147,103,                           # singles .                -
     71,123,119,143,                   # pairs   ..      .-       -.       --
    151,138,159, 83,111, 95,127, 99,   # threes  ... ..- .-. .--  -.. -.-  --. ---
    153, 88,  1,112,  0,128,105, 74,160, 76,164,170,132,  2,  3, 24,    # fours...
     20,  0, 16,  0,  0,  0, 12,  0,  0,  0,  0,  0,  0,  0,  8, 28,    # fives...
      0,  0,  0,  0,  0,  0,  0, 32,  0,  0,  0, 36,  0, 64,  4,  0]

# Bottom two bits encode whether another dash or dot (or either) gives a valid code
# if letter is finished, divide by four and add 48 to get the character-code

morse_step = 0
command = ''
busy = False
beeping = False
beepOn = 0
beepOff = 0

def obey(action):
    basic.show_string(action)

def decode(this):
    if this == '---':
        return 'S'
    elif  this == '...':
        return 'O'
    else:
        return ' '

def morse_dot():
    global morse_step
    v = MORSE_TABLE[-morse_step]
    if (v & 1) > 0:
        morse_step = (morse_step * 2) - 2
    else:
        morse_step = 0
    
def morse_dash():
    global morse_step
    v = MORSE_TABLE[-morse_step]
    if (v & 2) > 0:
        morse_step = (morse_step * 2) - 1
    else:
        morse_step = 0
        
def morse_end():
    global morse_step
    v = MORSE_TABLE[-morse_step] // 4
    if v > 0:
        morse_step = MORSE_TABLE[v+63] 
    else:
        morse_step = 0

    pass
                    
def morse_check():
    global busy, beeping, command
    if busy:
        if beeping:
            # if input.sound_level() < QUIET:
            if not input.button_is_pressed(Button.A):
                beepOff = control.millis()
                beeping = False
                # analyse length of beep that just stopped
                length = beepOff - beepOn
                if length > DASH_MIN:
                    morse_dash()
                elif length > DOT_MIN:
                    morse_dot()
            # ...else wait for the beep to stop
        else: # how long since last beep stopped?
            gap = control.millis() - beepOff
            if gap > LETTER_PAUSE:
                morse_end()
                busy = False
            # ...else keep listening for more dots or dashes
    else:
        # if input.sound_level() > LOUD:
        if input.button_is_pressed(Button.A):
            beepOn = control.millis()
            busy = True

def on_forever():
    # do all kinds of stuff...
    basic.show_icon(IconNames.HEART)
    # check for morse command
    morse_check()
    if morse_step > 0:
        obey(String.from_char_code(morse_step))
    basic.pause(20)
    

basic.forever(on_forever)