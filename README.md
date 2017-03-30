# raspyserver
A python webserver sample for fun (originally hosted in a raspberry pi)

Put all the files in /home/pi/Devel/raspyserver
(If you change this path, adjust accordingly in the ./pythonserver file)

Install requirements by running:
sudo ./setup.sh 

Then, run pythonserver with root access, 

sudo ./pythonserver

and your raspberry pi webserver is ready :-)

N.B. You may put the last command (/home/pi/pythonserver) in your /etc/rc.local file if you want the server to load on boot.
