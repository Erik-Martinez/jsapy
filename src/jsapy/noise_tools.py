from jsapy.noise import NoiseExposure

def noise_exposure(tasks, inf_action_value=None, sup_action_value=None, limit_value=None):
    
    noi = NoiseExposure(inf_action_value=inf_action_value, sup_action_value=sup_action_value, limit_value=limit_value)
    
    if not isinstance(tasks, list):
        raise TypeError(
            "Invalid input: 'tasks' must be a list of dictionaries.\n"
            "Example:\n"
            "[{'name': 'Metal Grinding', 'laeq_t': 94, 'time': 40},\n"
            " {'name': 'Jackhammering', 'laeq_t': 89, 'time': 160}, \n"
            " {'laeq_t': 70, 'time': 280}]"
        )
    
    exposures = []
    
    for idx, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            raise TypeError(f"Task entry #{idx} must be a dictionary.")
        
        name = task.get("name", f"Task {idx}")
        laeq_t = task.get("laeq_t")
        time = task.get("time")
        
        laeq_d = noi.calculate_laeq_d(id=name, laeq_t=laeq_t, exposure_time_minutes=time)
        exposures.append(laeq_d)
    
    return noi.calculate_total(exposures)