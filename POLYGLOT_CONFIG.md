
shortPoll: Not Used
longPoll: Not Used

Custom Parameters: 
url: The ip address of the iTach device 

All other custom params are user input devices with the Global Cache IR Codes
key: The Device i.e. "Onkyo Receiver"
value: A Global Cache Control Tower IR Database Format

An email from Global Cache with IR Codes look as follows, although there may be many more. The "function, code1, hexcode1, code2, hexcode2" is optional. When imputing the following commands, the custom param key: "Onkyo Receiver" and the value would be all codes for the device.

"
function, code1, hexcode1, code2, hexcode2

"3D","sendir,1:1,1,38000,1,1,171,171,21,65,21,65,21,65,21,21,21,21,21,21,21,21,21,21,21,65,21,65,21,65,21,21,21,21,21,21,21,21,21,21,21,65,21,65,21,65,21,65,21,65,21,21,21,21,21,65,21,21,21,21,21,21,21,21,21,21,21,65,21,65,21,21,21,1792","0000 006D 0000 0022 00AB 00AB 0015 0041 0015 0041 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0041 0015 0041 0015 0041 0015 0015 0015 0015 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0015 0015 0700",,

"ADD/DELETE","sendir,1:1,1,38000,1,1,170,170,22,64,22,64,22,64,21,22,21,22,21,22,21,22,21,22,21,65,21,65,21,65,21,22,21,22,21,22,21,22,21,22,21,65,21,22,22,22,21,65,21,65,21,22,21,22,21,22,22,22,21,65,21,65,21,22,21,22,21,65,21,65,21,65,21,1769","0000 006D 0000 0022 00AA 00AA 0016 0040 0016 0040 0016 0040 0015 0016 0015 0016 0015 0016 0015 0016 0015 0016 0015 0041 0015 0041 0015 0041 0015 0016 0015 0016 0015 0016 0015 0016 0015 0016 0015 0041 0015 0016 0016 0016 0015 0041 0015 0041 0015 0016 0015 0016 0015 0016 0016 0016 0015 0041 0015 0041 0015 0016 0015 0016 0015 0041 0015 0041 0015 0041 0015 06E9",,

"

How to obtain Global Cache Control Tower IR Codes:

Create an account and login to: 
https://irdb.globalcache.com/Home/Database

Enter the Brand Name of the device you would like to control. Then Select a Device Type, then Select a Model.

Now select the "Send Code Set" button next to the Device Model. Selecting "Select function" will only give you one code.

After receiving the email verify that you can see all IR Codes when scrolling to the bottom of the page. Gmail will clip the message and have a "Message clipped" not at the bottom of the page along with a View Entire Message button. Copy the entire message from the commas in the last IR Code to the beginning of the "function, code1, hexcode1, code2, hexcode2" header then paste into a new custom param value. Set the custom param key to the device name.

There may be multiple code sets that need to be downloaded or a single manufacture. Each Code set should be put into the Node Server Separately. This node serve is installed with the Onkyo Receiver Codes as an example
