#export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring -- надо применить как то


# Flash short guide

## get id
```
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg -c "init; scan_chain; shutdown"
```
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg -c "adapter usb scan" -c "shutdown"
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg -c "init" -c "jtag arp_init" -c "scan_chain" -c "shutdown"


openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg -c "init" -c "scan_chain" -c "shutdown" -- пока лучший
## flash
- insert id into cfg and run comm
```
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg    -f /usr/share/openocd/scripts/target/fpga.cfg -c "init; svf /home/adm/output.svf; shutdown"\”
```
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg -c "init" -c "reset halt" -c "flash write_image erase firmware.bin 0x08000000" -c "reset run" -c "shutdown"