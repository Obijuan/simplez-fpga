leds    EQU 507

        org h'100


loop    LD /val1
        ST /leds
        Wait
        ld /val2
        st /leds
        wait
        BR /loop

val1     DATA h'9
val2     DATA h'6

END
