import RPi.GPIO as GPIO
import time

#--------------------------------------------------------------------------
class gpio_relay :

   #--------------------------------------------------------------------------
   def __init__(self, mode, gpio_pins):
      self.m_gpio_pins = []
      for pin in gpio_pins:
         print "setup %s gpio class for %d" % (mode, pin)
         self.m_gpio_pins.append( pin)
         GPIO.setmode(GPIO.BCM)
         GPIO.setup( pin, GPIO.OUT)

   #--------------------------------------------------------------------------
   def enable(self, gpio_pin):
      gpio_pin = int(gpio_pin)
      if gpio_pin in self.m_gpio_pins:
         GPIO.output( gpio_pin, GPIO.LOW)
      else:
         raise Exception("GPIO pin %d not initialized!" % (gpio_pin))
      
   #--------------------------------------------------------------------------
   def disable(self, gpio_pin):
      gpio_pin = int(gpio_pin)
      if gpio_pin in self.m_gpio_pins:
         GPIO.output( gpio_pin, GPIO.HIGH)
      else:
         raise Exception("GPIO pin %d not initialized!" % (gpio_pin))
      
   #--------------------------------------------------------------------------
   def terminate( self):
      for pin in self.m_gpio_pins:
         gpio_relay.disable( self, pin)
      GPIO.cleanup()


#--------------------------------------------------------------------------
class usb_relay(gpio_relay) :

   #--------------------------------------------------------------------------
   def __init__(self, gpio_pin):
      self.m_usb_pin = int(gpio_pin)
      gpio_relay.__init__( self, "USB", [self.m_usb_pin])
      
   #--------------------------------------------------------------------------
   def enable(self):
#      print "Enable USB connection"
      gpio_relay.enable( self, self.m_usb_pin)
      
   #--------------------------------------------------------------------------
   def disable(self):
#      print "Disable USB connection"
      gpio_relay.disable( self, self.m_usb_pin)



#--------------------------------------------------------------------------
class fan_relay(gpio_relay) :

   #--------------------------------------------------------------------------
   def __init__(self, gpio_pin1, gpio_pin2, gpio_pin3, gpio_pin4):
      self.m_fan_volt1 = int(gpio_pin1)
      self.m_fan_on1 = int(gpio_pin2)
      self.m_fan_volt2 = int(gpio_pin3)
      self.m_fan_on2 = int(gpio_pin4)
      gpio_relay.__init__( self, "Fan", [self.m_fan_volt1, self.m_fan_on1, self.m_fan_volt2, self.m_fan_on2])

   #--------------------------------------------------------------------------
   def off(self):
      gpio_relay.disable( self, self.m_fan_volt1)
      gpio_relay.disable( self, self.m_fan_on1)
      gpio_relay.disable( self, self.m_fan_volt2)
      gpio_relay.disable( self, self.m_fan_on2)
      
   #--------------------------------------------------------------------------
   def slow(self):
      gpio_relay.disable( self, self.m_fan_volt1)
      gpio_relay.enable( self, self.m_fan_on1)
      gpio_relay.disable( self, self.m_fan_volt2)
      gpio_relay.disable( self, self.m_fan_on2)
      

   #--------------------------------------------------------------------------
   def medium(self):
      gpio_relay.disable( self, self.m_fan_volt1)
      gpio_relay.enable( self, self.m_fan_on1)
      gpio_relay.disable( self, self.m_fan_volt2)
      gpio_relay.enable( self, self.m_fan_on2)
      
   #--------------------------------------------------------------------------
   def fast(self):
      gpio_relay.disable( self, self.m_fan_volt1)
      gpio_relay.enable( self, self.m_fan_on1)
      gpio_relay.enable( self, self.m_fan_volt2)
      gpio_relay.enable( self, self.m_fan_on2)
      
   #--------------------------------------------------------------------------
   def ludicrous(self):
      gpio_relay.enable( self, self.m_fan_volt1)
      gpio_relay.enable( self, self.m_fan_on1)
      gpio_relay.enable( self, self.m_fan_volt2)
      gpio_relay.enable( self, self.m_fan_on2)
      


if __name__ == "__main__":
   usb=usb_relay(21)
   fan= fan_relay(26,19,13,6)
   fan.off()
   time.sleep(1)
   fan.slow()
   time.sleep(10)
   fan.medium()
   time.sleep(10)
   fan.fast()
   time.sleep(10)
   fan.ludicrous()
   time.sleep(10)
   fan.off()
#   usb.enable()
#   usb.terminate()
#---------------- End of file ------------------------------------------------

