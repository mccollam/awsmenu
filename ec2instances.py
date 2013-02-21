#!/usr/bin/env python
#
# AWS bits Copyright 2013 Ronald McCollam
# Author: Ronald McCollam <ronald
#
# Based on example code here:
#  http://developer.ubuntu.com/resources/technologies/application-indicators/
# Copyright 2009-2012 Canonical Ltd.
#
# Authors: Neil Jagdish Patel <neil.patel@canonical.com>
#          Jono Bacon <jono@ubuntu.com>
#          David Planella <david.planella@ubuntu.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of either or both of the following licenses:
#
# 1) the GNU Lesser General Public License version 3, as published by the
# Free Software Foundation; and/or
# 2) the GNU Lesser General Public License version 2.1, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the applicable version of the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of both the GNU Lesser General Public
# License version 3 and version 2.1 along with this program.  If not, see
# <http://www.gnu.org/licenses/>
#

# You need to set these to get this to work!
AWS_ACCESS_KEY = "SET ME"
AWS_SECRET_KEY = "SET ME TOO"

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from boto import ec2
import os
 
def ssh_to(w, buf):
  # The *right* thing to do here would be to say something like
  #    xdg-open ssh://buf
  # but sadly there's no ssh:// handler set up on Ubuntu by default
  os.system("x-terminal-emulator -e 'ssh " + buf + "' &")
 
if __name__ == "__main__":
  ind = appindicator.Indicator.new (
                        "ec2-select",
                        "start-here", #FIXME: need an icon!
                        appindicator.IndicatorCategory.APPLICATION_STATUS)
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)
#  ind.set_attention_icon ("indicator-messages-new") #TODO: Remove??
 
  # create a menu
  menu = Gtk.Menu()
 
  # Get a list of all running ec2 instances
  conn = ec2.connect_to_region("us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)
  reservations = conn.get_all_instances()

  for reservation in reservations:
    for instance in reservation.instances:
      if (instance.state_code == 16): # 16 == 'running'
        buf = instance.tags['Name']
        if (not buf):
          buf = instance.id
        menu_items = Gtk.MenuItem(buf)
        menu.append(menu_items)
        menu_items.connect("activate", ssh_to, instance.public_dns_name)
        menu_items.show()

  ind.set_menu(menu)
 
  Gtk.main()
