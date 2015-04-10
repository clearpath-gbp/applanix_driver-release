#! /usr/bin/env python
# -*- coding: utf-8 -*-
#     _____
#    /  _  \
#   / _/ \  \
#  / / \_/   \
# /  \_/  _   \  ___  _    ___   ___   ____   ____   ___   _____  _   _
# \  / \_/ \  / /  _\| |  | __| / _ \ | ┌┐ \ | ┌┐ \ / _ \ |_   _|| | | |
#  \ \_/ \_/ /  | |  | |  | └─┐| |_| || └┘ / | └┘_/| |_| |  | |  | └─┘ |
#   \  \_/  /   | |_ | |_ | ┌─┘|  _  || |\ \ | |   |  _  |  | |  | ┌─┐ |
#    \_____/    \___/|___||___||_| |_||_| \_\|_|   |_| |_|  |_|  |_| |_|
#            ROBOTICS™
#
#
#  Copyright © 2012 Clearpath Robotics, Inc. 
#  All Rights Reserved
#  
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Clearpath Robotics, Inc. nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CLEARPATH ROBOTICS, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Please send comments, questions, or patches to skynet@clearpathrobotics.com
#

# ROS
import rospy

# ROS messages and services
import applanix_msgs.srv
import applanix_msgs.msg

# Node
from port import Port
from handlers import AckHandler
from applanix_msgs import mapping

# Python
import threading
from cStringIO import StringIO


SILENCE_INTERVAL=5.0


class ControlPort(Port):
  def run(self):
    self.sock.setblocking(1)
    self.services_ready = threading.Event()
    self.services = []
    self.lock = threading.Lock()
    self.last_transaction_number = 0

    for msg_num in mapping.msgs.keys():
      if msg_num != 0:
        self.services.append(ServiceHandler(msg_num, self))
    self.services_ready.set()
    
    # Send the navigation mode every n seconds so that the Applanix device
    # doesn't close the connection on us.
    set_nav_mode = rospy.ServiceProxy("nav_mode", applanix_msgs.srv.SetNavModeControl)
    nav_mode_msg = applanix_msgs.msg.NavModeControl(mode=applanix_msgs.msg.NavModeControl.MODE_NAVIGATE)
    while not self.finish.is_set():
      rospy.sleep(SILENCE_INTERVAL)
      set_nav_mode(nav_mode_msg)

  def next_transaction(self):
    self.last_transaction_number += 1
    return self.last_transaction_number


class ServiceHandler(object):
  def __init__(self, msg_num, port):
    self.name, data_class = mapping.msgs[msg_num]
    self.port = port
    self.service = rospy.Service(self.name, getattr(applanix_msgs.srv, "Set" + data_class.__name__), self.handle)

    # Part of the outbound message to Applanix device.
    self.header = applanix_msgs.msg.CommonHeader(start=applanix_msgs.msg.CommonHeader.START_MESSAGE, id=msg_num, length=0)

  def handle(self, message):
    # Called on the service's own thread, so acquire lock before using control socket.
    # Hold lock until entire interaction is complete, so that we guarantee the next message
    # received is our ack.
    with self.port.lock:
      # Write request to self.sock
      message.request.transaction = self.port.next_transaction() 
      self.port.send(self.header, message.request)

      # Read response from port, return it.
      pkt_id, pkt_str = self.port.recv()
      
      if pkt_id == None:
        raise ValueError("No response message on control port.")

      if pkt_id != (applanix_msgs.msg.CommonHeader.START_MESSAGE, 0):
        raise ValueError("Non-ack message on control port: %s.%d" % pkt_id)

      handler = AckHandler()
      handler.handle(StringIO(pkt_str))

      return handler.message
