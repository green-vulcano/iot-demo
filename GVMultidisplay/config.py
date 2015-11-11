# 7 Segment Display configuration
cfg = {
    "device" : {
        "id"        : "GVDEV004",
        "name"      : "GV Multi Display",
        "ip"        : "10.100.80.39",
        "server_ip" : "10.100.80.39"
    },
    "segment1"  : {
        "data"  : 35,
        "clock" : 32,
        "latch" : 37
    },
    "segment2"  : {
        "data"  : 33,
        "clock" : 32,
        "latch" : 23
    },
    "segment3"  : {
        "data"  : 31,
        "clock" : 32,
        "latch" : 21
    },
    "segment4"  : {
        "data"  : 29,
        "clock" : 32,
        "latch" : 19
    },
    "lcd_top" : {
        "rs" : 16,
        "e"  : 18,
        "d4" : 24,
        "d5" : 22,
        "d6" : 12,
        "d7" : 26,
        "width" : 16,
        "chr" : True,
        "cmd" : False
    },
    "lcd_bottom" : {
        "rs" : 5,
        "e"  : 3,
        "d4" : 7,
        "d5" : 11,
        "d6" : 13,
        "d7" : 15,
        "width" : 16,
        "chr" : True,
        "cmd" : False
    },
    "rgb_led" : {
        "red" :     38,
        "green" :   40,
        "blue" :    36
    }
}

charset = {
    " " : 0b00000000,
    "." : 0b10000000,
    "0" : 0b01111110, 
    "1" : 0b00110000, 
    "2" : 0b01011011, 
    "3" : 0b01111001, 
    "4" : 0b00110101, 
    "5" : 0b01101101, 
    "6" : 0b01101111, 
    "7" : 0b00111000, 
    "8" : 0b01111111, 
    "9" : 0b01111101,
    "a" : 0b00111111,
    "b" : 0b01100111,
    "c" : 0b01001110,
    "d" : 0b01110011,
    "e" : 0b01001111,
    "f" : 0b00001111,
    "g" : 0b01111101,
    "h" : 0b00110111,
    "i" : 0b00000110,
    "j" : 0b01110010,
    "l" : 0b01000110,
    "m" : 0b00101010,
    "n" : 0b00100011,
    "o" : 0b01111110,
    "p" : 0b00011111,
    "q" : 0b00111101,
    "r" : 0b00000011,
    "s" : 0b01101101,
    "t" : 0b01000111,
    "u" : 0b01110110,
    "v" : 0b01110110,
    "y" : 0b01110101,
    "z" : 0b01011011
}

colorset = {
    "red" :     "FF0000",
    "violet" :  "FF3399",
    "green" :   "00FF00",
    "blue" :    "0000FF",
    "azure" :   "66FFFF",
    "yellow" :  "FFCC00",
    "off":      "000000"
}