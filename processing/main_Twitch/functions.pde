class ONS_instance {
  boolean trigger, memory, pulse = false;
  Boolean run() {
    if (trigger == true && memory == false) {
      pulse = true;
    } 
    else { 
      pulse = false;
    }
    memory = trigger;
    return pulse;
  }
  Boolean run(Boolean i_trigger) {
    trigger = i_trigger;
    return run();
  }
}

float clamp_f(float input, float limit_low, float limit_high) {
  if (input > limit_high) {
    input = limit_high;
  }
  else if (input < limit_low) {
    input = limit_low;
  }
  return input;
}