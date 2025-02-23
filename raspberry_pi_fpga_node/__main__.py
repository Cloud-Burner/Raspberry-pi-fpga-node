#
# from openocd import OpenOcd
#
# with OpenOcd() as oocd:
#     oocd.halt()
#     registers = oocd.read_registers(['pc', 'sp'])
#
#     print('Program counter: 0x%x' % registers['pc'])
#     print('Stack pointer: 0x%x' % registers['sp'])
#
#     oocd.resume()

from openocd import OpenOcd
with OpenOcd() as oocd:
    oocd.halt()
    registers = oocd.read_registers(['pc', 'sp'])
    oocd.execu te("openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg    -f /usr/share/openocd/scripts/target/fpga.cfg -c "init; svf /home/adm/output.svf; shutdown"\”")

    print('Program counter: 0x%x' % registers['pc'])
    print('Stack pointer: 0x%x' % registers['sp'])

    oocd.resume()