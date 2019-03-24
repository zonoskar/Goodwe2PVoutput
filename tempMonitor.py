import goodweData
import gpio
  
class tempMonitor :

   #--------------------------------------------------------------------------
   def __init__( self, goodweData, fan_pins):
   #Initialization of the goodweData class. All data members are set
      goodweData.subscribe_temperature( self.temperature_callback)
      self.fan = gpio.fan_relay( fan_pins[0], fan_pins[1], fan_pins[2], fan_pins[3])
      self.counter = 4
      self.prevSpeed = 0
      self.fan.off()
      
   #--------------------------------------------------------------------------
   def temperature_callback( self, temperature):
      speed = 0
      if temperature > 50:
         speed = 4
      elif temperature > 45:
         speed = 3
      elif temperature > 40:
         speed = 2
      elif temperature > 35:
         speed = 1
      else:
         speed = 0
         
      self._switch_fan_speed( speed)
      self.prevSpeed = speed
      
   def _switch_fan_speed( self, speed):
      if self.prevSpeed < speed or self.counter <= 0:
         print "Setting fan speed " + str(speed) 
         self._set_fan_speed( speed)
         self.counter = 4
      else:
         print "Fan speed " + str(self.prevSpeed) + " at counter " + str(self.counter)
         self.counter -= 1
         
   def _set_fan_speed( self, speed):
      if speed == 4:
         self.fan.ludicrous()
      elif speed == 3:
         self.fan.fast()
      elif speed == 2:
         self.fan.medium()
      elif speed == 1:
         self.fan.slow()
      else:
         self.fan.off()
   
#---------------- End of file ------------------------------------------------
