from jsapy.vibrations import HandArmVibrations, CompleteBodyVibrations


def vibrations_hand_arm(machines, action_value=None, limit_value=None):
    """
    Calculate the daily hand-arm vibration exposure A(8) for multiple machines.

    This function estimates the total vibration exposure using either 
    the vibration total value `aw` or the three orthogonal acceleration 
    components `ax`, `ay`, and `az`, according to the user's input for 
    each machine. Exposure is calculated based on the weighted average 
    over time and assessed against the defined action and limit values.

    Parameters
    ----------
    machines : list of dict
        A list of dictionaries, where each dictionary represents a machine and must
        contain vibration data and exposure time. Each dictionary must include:

        - Either:
            - `aw` : float
                Vibration total value in m/s².
          OR
            - `ax` : float
              X-axis vibration component in m/s².
            - `ay` : float
              Y-axis vibration component in m/s².
            - `az` : float
              Z-axis vibration component in m/s².
        
        - `time` : float
            Daily exposure time for the machine in hours.

        - `name` : str, optional
            Name or identifier of the machine. If not provided, a default name
            like "Machine 1", "Machine 2", etc., is assigned automatically.

        All numeric values must be non-negative. Exposure time must be greater
        than zero.

    action_value : float, optional
        Exposure action value A(8) in m/s². If not provided, the default value of 2.5 is used.

    limit_value : float, optional
        Exposure limit value A(8) in m/s². If not provided, the default value of 5.0 is used.

    Returns
    -------
    VibraResult
        An object containing the calculated daily exposure A(8), the unit,
        and flags indicating whether the exposure exceeds the action or limit value.

    Raises
    ------
    TypeError
        If `machines` is not a list or any element in the list is not a dictionary.
    ValueError
        If required keys are missing or if both `aw` and `ax/ay/az` are provided
        simultaneously for a single machine.

    See Also
    --------
    HandArmVibrations : Class used to perform hand-arm vibration calculations.
    VibraResult : Class for storing and formatting the vibration exposure result.

    Examples
    --------
    >>> import jsapy as jsa
    >>> machines = [
    ...     {"name": "Pneumatic Drill", "ax": 1.0, "ay": 1.2, "az": 0.9, "time": 3},
    ...     {"aw": 1.6, "time": 2},  # unnamed → "Machine 2"
    ... ]
    >>> result = jsa.vibrations_hand_arm(machines)
    >>> print(result)
    1.363

    >>> jsa.display(result)
    --- Hand-Arm Vibration Exposure Assessment ---
    A(8) vibration value: 1.363 m/s².
    Exposure is below the action value.
    No specific action is required.
    """
    if not isinstance(machines, list):
        raise TypeError(
            "Invalid input: 'machines' must be a list of dictionaries.\n"
            "Example:\n"
            "[{'name': 'Drill', 'ax': 2.0, 'ay': 1.5, 'az': 1.0, 'time': 2.0},\n"
            " {'name': 'Grinder', 'aw': 3.2, 'time': 1.5}, \n"
            " {'aw': 2.0, 'time': 0.5}]"
        )
    
    vib = HandArmVibrations(action_value=action_value, limit_value=limit_value)
    exposures = []
    
    for idx, machine in enumerate(machines, start=1):
        if not isinstance(machine, dict):
            raise TypeError(f"Machine entry #{idx} must be a dictionary.")
        
        name = machine.get("name", f"Machine {idx}")
        aw = machine.get("aw")
        ax = machine.get("ax")
        ay = machine.get("ay")
        az = machine.get("az")
        time = machine.get("time")
        
        a8 = vib.calculate_a8(id=name, ax=ax, ay=ay, az=az, aw= aw, exposure_time_hours=time)
        exposures.append(a8)
        
    return vib.calculate_total(exposures)
 
        
def vibrations_body(machines, action_value=None, limit_value=None):
    """
    Calculate the daily whole-body vibration exposure A(8) for multiple machines.

    This function estimates the total whole-body vibration exposure using 
    the three orthogonal acceleration components `ax`, `ay`, and `az` for each 
    machine, according to ISO 2631-1 weighting factors. The function calculates 
    the frequency-weighted RMS acceleration over time and determines the 
    maximum value among the axes, which is compared against the defined 
    action and limit values.

    Parameters
    ----------
    machines : list of dict
        A list of dictionaries, where each dictionary represents a machine and must
        contain vibration data and exposure time. Each dictionary must include:

        - `ax` : float  
            X-axis vibration component in m/s².
        - `ay` : float  
            Y-axis vibration component in m/s².
        - `az` : float  
            Z-axis vibration component in m/s².
        - `time` : float  
            Daily exposure time for the machine in hours.
        - `name` : str, optional  
            Name or identifier of the machine. If not provided, a default name
            like "Machine 1", "Machine 2", etc., is assigned automatically.

        All numeric values must be non-negative. Exposure time must be greater than zero.

    action_value : float, optional
        Exposure action value A(8) in m/s². If not provided, the default value of 0.5 is used.

    limit_value : float, optional
        Exposure limit value A(8) in m/s². If not provided, the default value of 1.15 is used.

    Returns
    -------
    VibraResult
        An object containing the calculated daily exposure A(8), the unit,
        and flags indicating whether the exposure exceeds the action or limit value.

    Raises
    ------
    TypeError
        If `machines` is not a list or any element in the list is not a dictionary.
    ValueError
        If required keys (`ax`, `ay`, `az`, `time`) are missing or contain invalid values.

    See Also
    --------
    CompleteBodyVibrations : Class used to perform whole-body vibration calculations.
    VibraResult : Class for storing and formatting the vibration exposure result.

    Examples
    --------
    >>> import jsapy as jsa
    >>> machines = [
    ...     {"name": "Forklift", "ax": 0.6, "ay": 0.5, "az": 0.4, "time": 3},
    ...     {"name": "Compactor", "ax": 1.0, "ay": 1.2, "az": 0.9, "time": 2}
    ... ]
    >>> result = jsa.vibrations_body(machines)
    >>> print(result)
    0.943

    >>> jsa.display(result)
    --- Complete Body Vibration Exposure Assessment ---
    A(8) vibration value: 0.943 m/s².
    Danger: Exposure exceeds the **Exposure Action Value (0.5m/s²)**.
    Preventive measures should be implemented to control exposure.
    """
    
    if not isinstance(machines, list):
        raise TypeError(
            "Invalid input: 'machines' must be a list of dictionaries.\n"
            "Example:\n"
            "[{'name': 'Compactor', 'ax': 2.0, 'ay': 1.5, 'az': 1.0, 'time': 2.0},\n"
            " {'name': 'Forklift', 'ax': 1.0, 'ay': 1.2, 'az': 0.9, 'time': 3}, \n"
            " {'ax': 1.0, 'ay': 1.2, 'az': 0.9, 'time': 2.0}]"
        )
        
    vib = CompleteBodyVibrations(action_value=action_value, limit_value=limit_value)
    exposure_x = []
    exposure_y = []
    exposure_z = []
           
    for idx, machine in enumerate(machines, start=1):
        if not isinstance(machine, dict):
            raise TypeError(f"Machine entry #{idx} must be a dictionary.")
        
        name = machine.get("name", f"Machine {idx}")
        ax = machine.get("ax")
        ay = machine.get("ay")
        az = machine.get("az")
        time = machine.get("time")
        
        Ax, Ay, Az = vib.calculate_A_vertex(id=name, ax=ax, ay=ay, az=az, exposure_time_hours=time)
        exposure_x.append(Ax)
        exposure_y.append(Ay)
        exposure_z.append(Az)
        
    return vib.calculate_total(exposure_x, exposure_y, exposure_z)