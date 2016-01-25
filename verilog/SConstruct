import os

# -- Nombre del fichero a ensamblar
NAME = 'simplez'
DEPS_str = 'simplez.v genram.v {0}/dividerp1.v {0}/uart_tx.v {0}/baudgen_tx.v \
            {0}/uart_rx.v {0}/baudgen_rx.v'.format('peripherals')
DEPS = Split(DEPS_str)
PCF = NAME + '.pcf'

# -- Constructor para sintetizar
synth = Builder(action='yosys -p \"synth_ice40 -blif $TARGET\" $SOURCES',
                suffix='.blif',
                src_suffix='.v')

pnr = Builder(action='arachne-pnr -d 1k -o $TARGET -p {} $SOURCE'.format(PCF),
              suffix='.asc',
              src_suffix='.blif')

bitstream = Builder(action='icepack $SOURCE $TARGET',
                    suffix='.bin',
                    src_suffix='.asc')

# -- Construccion del informe de tiempos
time_rpt = Builder(action='icetime -mtr $TARGET $SOURCE',
                   suffix='.rpt',
                   src_suffix='.asc')

# -- Construir el entorno
env = Environment(BUILDERS={'Synth': synth, 'PnR': pnr, 'Bin': bitstream, 'Time': time_rpt})


# -- Sintesis complesta: de verilog a bitstream
blif = env.Synth(NAME, DEPS)
asc = env.PnR([blif, PCF])
Default(env.Bin(asc))

# -- Objetivo time para calcular el tiempo
rpt = env.Time(asc)
t = env.Alias('time', rpt)


# ----------- Entorno para simulacion

# -- Constructor para generar simulacion: icarus Verilog
iverilog = Builder(action='iverilog $SOURCES -o $TARGET',
                   suffix='.out',
                   src_suffix='.v')

vcd = Builder(action='./$SOURCE', suffix='.vcd', src_suffix='.out')

# -- Create the simulation environment. All the environment variables are included
# -- (if not, there is an error executing gtkwave)
simenv = Environment(BUILDERS={'IVerilog': iverilog, 'VCD': vcd},
                     ENV=os.environ)

TB = NAME+'_tb'
out = simenv.IVerilog(NAME+'_tb', Split(DEPS_str+' '+TB+'.v'))
vcd_file = simenv.VCD(out)


gtkwave = simenv.Alias('sim', vcd_file, 'gtkwave $SOURCE '+TB+'.gtkw'+' &')
AlwaysBuild(gtkwave)

# -- These is for cleaning the files generated using the alias targets
if GetOption('clean'):
    env.Default(t)
    env.Default(gtkwave)
