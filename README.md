awsmenu
=======

A Unity indicator for quick access to AWS services

Currently all that it does is get a list of your running EC2 instances and put
them in an indicator.  Clicking the name of the instance will open a terminal
and ssh to the instance.

Before using this, you need to edit ec2instances.py and set your AWS access
key and AWS secret key.  You will also need the python-boto library installed.
On Ubuntu you can simply say:
  sudo apt-get install python-boto

Usage:
python ec2instances.py &
