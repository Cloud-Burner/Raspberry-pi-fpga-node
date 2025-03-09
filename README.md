
# Flash short guide

## get id
```
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg -c "init; scan_chain; shutdown"
```

## flash
- insert id into cfg and run comm
```
openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg    -f /usr/share/openocd/scripts/target/fpga.cfg -c "init; svf /home/adm/output.svf; shutdown"\”
```

