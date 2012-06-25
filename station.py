import gi
import sys

try:
	gi.require_version('Gst','1.0')
except ValueError:
	print 'Could not find required Gstreamer library'
	sys.exit(1)

from gi.repository import Gst, GstVideo
print Gst.version_string()

class Station(object):
	def __init__(self):
		Gst.init(None)
				
		self.pipeline = Gst.Pipeline()

		src = Gst.ElementFactory.make('v4l2src', None)
		caps_filter = Gst.ElementFactory.make('capsfilter', None)
		self.sink = Gst.ElementFactory.make('xvimagesink', None)

		caps_filter.set_property('caps',Gst.caps_from_string("video/x-raw, width=640, height=480"))

		self.pipeline.add(src)
		self.pipeline.add(caps_filter)
		self.pipeline.add(self.sink)

		src.link(caps_filter)
		caps_filter.link(self.sink)

		bus = self.pipeline.get_bus()
		bus.connect('message::eos', self.on_bus_eos)
		bus.connect('message', self.on_bus_message)
		bus.add_signal_watch()
		
	def swap(self):
		# Test hotswap of v4l2src and videotestsrc
		pass
		
	def assign_drawing_area(self, drawing_area):
		print "DrawingArea ID: " + str(drawing_area.get_window().get_xid())
		self.sink.set_window_handle(drawing_area.get_window().get_xid())

	def on_bus_message(self, bus, message):
		pass
		
	def on_bus_eos(self, bus, message):
		print "EOS Received"
		print message
		self.stop()
	
	def run(self):
		self.pipeline.set_state(Gst.State.PLAYING)
		
	def stop(self):
		self.pipeline.set_state(Gst.State.NULL)
