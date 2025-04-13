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
    0x020f10dd

    s3_url: str = "http://192.168.1.39:9000"

sudo apt install libopencv-dev python3-opencv

## test msg
{"username": "maks", "flash_file": "pins_output1.svf", "instruction_file": "exz.txt", "number": "123"}
# on board config 


"""This module contains the settings for the all app"""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
"""This module contains the settings for the all app"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for the Raspberry Pi Fpga node"""

    rabbit_host: str = "192.168.1.39"
    rabbit_port: int = 5672
    green_board_q: str = "green_1"
    result_exc: str = "result"

    log_level: str = "info"
    max_threads: int = 3
    camera_number: int = 0
    fourcc_codec: str = "mp4v"
    video_format: str = "mp4"
    fps: int = 20

    fpga_address: str = "ax9999"
    fpga_camera_position: Literal[0, 1] = 1

    s3_url: str = "http://192.168.1.39:9000"
    access_key: str = "f0Sxs0Bf2pqJDQtFNQZF"
    secret_key: str = "hrGuLOhzFZBNWtmL5TJ8wiB2e5d9jIHeSzdEYXbW"
    result_bucket: str = "test"
    task_bucket: str = "test"

    project_dir: str = str(Path.cwd())
    dynamic_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/dynamic_files"
    static_dir: str = project_dir + "/raspberry_pi_fpga_node/processing/static_confs"


settings = Settings()
print(settings.project_dir)



right target 
adapter speed 1000
jtag newtap auto0 tap  -expected-id 0x020f10dd -irlen 10


openocd -f /usr/share/openocd/scripts/interface/altera-usb-blaster.cfg    -f /usr/share/openocd/scripts/target/fpga.cfg -c "init; svf /home/adm/output.svf; shutdown"\”


settings = Settings()

