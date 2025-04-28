# Cece Espadas - Project 3
# ECE 2774
# Synchronous Condenser

class SynchronousCondenser:
    def __init__(self, name, bus, q_max):

        self.name = name   # Unique name identifier for this synchronous condenser
        self.bus = bus # The bus object to which this SynCon is physically connected
        self.q_max = q_max # Maximum reactive power output in MVAR (positive Q → sourcing vars)
        self.q_min = -1 * q_max / 2 # Minimum reactive power output in MVAR (negative Q → absorbing vars)
        # Conventionally set to half the maximum but negative (absorbing capability)
        self.vset = bus.base_kv  # Voltage setpoint in kV — initialized from the current bus voltage

    def enforce_q_limits(self, q_output):
        """
        This method enforces the reactive power (Q) operating limits of the SynCon.

        Parameters:
        - q_output (float): The attempted reactive power output in MVAR

        Returns:
        - (float, bool): The clipped Q output (within min/max)
                         and a flag indicating whether limiting occurred.
        """

        # If the requested Q is below the minimum allowed (absorbing too much), clamp it
        if q_output < self.q_min:
            return self.q_min, True

        # If the requested Q is above the maximum allowed (producing too much), clamp it
        elif q_output > self.q_max:
            return self.q_max, True

        # Otherwise, Q is within the acceptable range — return unchanged
        return q_output, False
