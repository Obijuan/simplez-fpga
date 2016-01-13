LEDS    EQU 507

        org h'100

        LD /val
        ST /LEDS
        HALT

val     DATA h'7

END
