from datetime import datetime
from datetime import timedelta

class ONS_instance:

   def __init__(self):
      self.trigger, self.memory, self.pulse = False

   def run(self, *args):
      if len(args) == 0:
         pass
      if len(args) == 1:
         self.trigger = args[0]
      if len(args) > 1:
         raise Exception('ONS function used wrong!')

      if (self.trigger == True and self.memory == False):
         self.pulse = True
      else: 
         self.pulse = False

      self.memory = self.trigger
      return self.pulse

# returns the elapsed milliseconds since the start of the program
class ElapseTracker:

   def __init__(self):
      self.start_time = datetime.now()
      self.dt = 0

   def curr(self):
      self.dt = datetime.now() - self.start_time
      ms = (self.dt.days * 24 * 60 * 60 + self.dt.seconds) * 1000 + self.dt.microseconds / 1000.0
      return ms

class TimerON:

   def __init__(self):
      self.timeKept = ElapseTracker()
      self.preset = 0
      self.accumulated = 0
      self.timing = False
      self.done = False
      self.enable = False
      self.pulseDone = False

   # Timing run() may pass 0, 1, or 2 arguments:
   # run() will use accessible .enable, .preset
   # run(arg) will look for a single boolean True/ False to enable running
   # run(arg, arg) will look for the same as above with the second being an integer for preset time
   def run(self, *args ):

      self.pulseDone = False

      # Evaluate arguments
      exceptFound = False
      if len(args) >= 1:
         if type(args[0] == bool):
            self.enable = args[0]
         else:
            exceptFound = True
      if len(args) == 2:
         if type(args[1] == int):
            if args[1] >= 0:
               self.preset = args[1]
            else:
               exceptFound = True
         else:
            exceptFound = True
      if len(args) > 2:
         exceptFound = True

      if exceptFound:
         raise Exception('TimerON function used wrong!')

      # initialize time elapse function on start of enable

      if self.enable and not self.timing and not self.done:
         self.timeKept = ElapseTracker()
      
      if self.enable:
         if not self.done:
            self.accumulated = self.timeKept.curr()
            if self.accumulated >= self.preset:
               self.done = True
               self.pulseDone = True
            self.timing = not self.done

      else:
         self.done = False
         self.timing = False

      return self.done

   def reset(self):
      self.accumulated = False
      self.done = False
      self.timing = False