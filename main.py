#!/usr/bin/env python
# Using ppa: https://launchpad.net/~o-naudan/+archive/gst0.11

import gi
import sys
import station
import json

from gi.repository import GObject, Gtk, Gdk, GdkX11

class Main:
	def __init__(self):
		GObject.threads_init()

 		config_text = open('config.json').read()
		self.config = json.loads(config_text)

		win = Gtk.Window()
		button = Gtk.Button(label="Do Something")
		win.add(button)
		win.show_all()
		
		win.connect("delete-event", self.on_quit)
		
		self.station = station.Station(self.config)
		
		self.displays = {}
		for display_details in self.config["displays"]:
			self.create_display(display_details["name"],
								display_details["monitor"],
								display_details["location"])

	def create_display(self,name,monitor,location):
		display_window = Gtk.Window()
		self.displays[name] = display_window

		drawing_area = Gtk.DrawingArea()
		drawing_area.set_size_request(640,480)
		drawing_area.connect("realize", self.on_video_window_realize, monitor)
		
		display_window.add(drawing_area)
		drawing_area.show()
		display_window.show_all()

	def on_video_window_realize(self, drawing_area, monitor):
		self.station.assign_drawing_area(drawing_area, monitor)
	
	def run(self):
		self.station.run()
		Gtk.main()
		
	def on_quit(self, event, user_data):
		self.station.stop()
		Gtk.main_quit()

if __name__ == "__main__":
	Main().run()
