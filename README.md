# DMR-5200 Interface Library

This is a simple library to read and format data from the serial interface on a
[Circuit-Test DMR-5200][1] digital multimeter. The connection settings and data
format for the meter are described in Section 8 of the DMR-5200 manual.

The included `dmr5200` script illustrates how to use the library, and can be
used as a simple tool to generate CSV formatted readings from a connected
multimeter.

The library assumes that the multimeter has already been put into RS-232 mode
using the procedure described in Section 8 of the manual.

[1]: <http://www.circuittest.com/dmr-5200-dmm-digital-multimeter-true-rms-computer-interface.html>  "Circuit-Test DMR-5200"

## dmr5200 Script Usage

    dmr5200 <serial_port> <request_interval>

Where `serial_port` is the serial device that the multimeter is connected to,
and `request_interval` is the floating point polling interval in seconds.  The
meter generally takes a second or two to process and respond to each request, so
setting an interval below about 2 seconds will have little effect.

The command

    dmr5200 /dev/ttyUSB0 5

will take a reading every 7 seconds or so (allowing for the meter processing
time) from the meter connected to `/dev/ttyUSB0` and write it as a comma
separated record to stdout.

The CSV format is as follows:

    function,value,units,timestamp

and the first line printed has the comma separated column headings.
