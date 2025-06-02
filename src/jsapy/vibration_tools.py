from jsapy.vibrations import HandArmVibrations


def vibrations_hand_arm(machines, action_value=None, limit_value=None):
    """machines = [
    {"name": "Pistola neumática", "ax": 1.0, "ay": 1.2, "az": 0.9, "time": 3},
    {"aw": 1.6, "time": 2},  # sin nombre → "Machine 2"
    ]
    """
    if not isinstance(machines, list):
        raise TypeError(
            "Invalid input: 'machines' must be a list of dictionaries.\n"
            "Example:\n"
            "[{'name': 'Taladro', 'ax': 2.0, 'ay': 1.5, 'az': 1.0, 'time': 2.0},\n"
            " {'name': 'Pulidora', 'aw': 3.2, 'time': 1.5}, \n"
            " {'aw': 2.0, 'time': 0.5}"
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
        
        