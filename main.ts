function obey(str: any) {
    
}

function decode(str: string): string {
    
}

function morse_check(): string {
    let beepOff: number;
    let beeping: boolean;
    let length: number;
    let gap: number;
    let listening: boolean;
    let beepOn: number;
    let letter = "?"
    let pattern = ""
    if (listening) {
        if (beeping) {
            if (input.soundLevel() < QUIET) {
                beepOff = control.millis()
                beeping = false
                //  analyse length of beep that just stopped
                length = beepOff - beepOn
                if (length > DASH) {
                    pattern += "-"
                } else {
                    pattern += "."
                }
                
            }
            
        } else {
            //  else just let the beep continue...
            //  how long since last beep stopped?
            gap = control.millis() - beepOff
            if (gap > LETTER) {
                listening = false
                letter = decode(pattern)
                pattern = ""
            }
            
        }
        
    } else if (input.soundLevel() > LOUD) {
        beepOn = control.millis()
        listening = true
    }
    
    return letter
}

let DASH = 500
let LETTER = 1000
let LOUD = 200
let QUIET = 100
let listening = false
let beeping = false
let beepOn = 0
basic.forever(function on_forever() {
    //  do all kinds of stuff...
    basic.showIcon(IconNames.Heart)
    //  check for morse command
    let letter = morse_check()
})
