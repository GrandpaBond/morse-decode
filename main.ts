let DOT_MIN = 200
let DASH_MIN = 500
let LETTER_PAUSE = 1000
let LOUD = 200
let QUIET = 100
let MORSE_TABLE = [87, 147, 103, 71, 123, 119, 143, 151, 138, 159, 83, 111, 95, 127, 99, 153, 88, 1, 112, 0, 128, 105, 74, 160, 76, 164, 170, 132, 2, 3, 24, 20, 0, 16, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 8, 28, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 36, 0, 64, 4, 0]
//  binary tree of state values:
//  singles .                -
//  pairs   ..      .-       -.       --
//  threes  ... ..- .-. .--  -.. -.-  --. ---
//  fours...
//  fives...
//  Bottom two bits encode whether another dash or dot (or either) gives a valid code
//  if letter is finished, divide by four and add 48 to get the character-code
let morse_step = 0
let command = ""
let busy = false
let beeping = false
let beepOn = 0
let beepOff = 0
function obey(action: string) {
    basic.showString(action)
}

function decode(this_: any): string {
    if (this_ == "---") {
        return "S"
    } else if (this_ == "...") {
        return "O"
    } else {
        return " "
    }
    
}

function morse_dot() {
    
    let v = MORSE_TABLE[-morse_step]
    if ((v & 1) > 0) {
        morse_step = morse_step * 2 - 2
    } else {
        morse_step = 0
    }
    
}

function morse_dash() {
    
    let v = MORSE_TABLE[-morse_step]
    if ((v & 2) > 0) {
        morse_step = morse_step * 2 - 1
    } else {
        morse_step = 0
    }
    
}

function morse_end() {
    
    let v = Math.idiv(MORSE_TABLE[-morse_step], 4)
    if (v > 0) {
        morse_step = MORSE_TABLE[v + 63]
    } else {
        morse_step = 0
    }
    
    
}

function morse_check() {
    let beepOff: number;
    let length: number;
    let gap: number;
    let beepOn: number;
    
    if (busy) {
        if (beeping) {
            //  if input.sound_level() < QUIET:
            if (!input.buttonIsPressed(Button.A)) {
                beepOff = control.millis()
                beeping = false
                //  analyse length of beep that just stopped
                length = beepOff - beepOn
                if (length > DASH_MIN) {
                    morse_dash()
                } else if (length > DOT_MIN) {
                    morse_dot()
                }
                
            }
            
        } else {
            //  ...else wait for the beep to stop
            //  how long since last beep stopped?
            gap = control.millis() - beepOff
            if (gap > LETTER_PAUSE) {
                morse_end()
                busy = false
            }
            
        }
        
    } else if (input.buttonIsPressed(Button.A)) {
        beepOn = control.millis()
        busy = true
    }
    
}

basic.forever(function on_forever() {
    //  do all kinds of stuff...
    basic.showIcon(IconNames.Heart)
    //  check for morse command
    morse_check()
    if (morse_step > 0) {
        obey(String.fromCharCode(morse_step))
    }
    
    basic.pause(20)
})
