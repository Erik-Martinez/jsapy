from jsapy.noise import NoiseExposure

def noise_exposure(tasks, inf_action_value=None, sup_action_value=None, limit_value=None):
    """
    Calculate the daily noise exposure LAeq,d from multiple noise-emitting tasks.

    This function estimates the total daily noise exposure based on the 
    equivalent continuous sound level (LAeq,T) and the exposure duration 
    of each task. It aggregates all tasks and assesses the final LAeq,d 
    value against predefined regulatory thresholds.

    Parameters
    ----------
    tasks : list of dict
        A list of dictionaries, each representing a task involving noise 
        exposure. Each dictionary must include:

        - 'laeq_t' : float  
            The equivalent continuous sound level during the task (in dB(A)).
        
        - 'time' : float  
            Duration of the task in minutes.
        
        - 'name' : str, optional  
            Name or identifier of the task. If not provided, a default label 
            like "Task 1", "Task 2", etc., is assigned automatically.

        Example:
        [
            {"name": "Metal Grinding", "laeq_t": 94, "time": 40},
            {"name": "Jackhammering", "laeq_t": 89, "time": 160},
            {"laeq_t": 70, "time": 280}  # unnamed → "Task 3"
        ]

    inf_action_value : float, optional
        Lower action value (in dB(A)). If not specified, defaults to 80 dB(A).

    sup_action_value : float, optional
        Upper action value (in dB(A)). If not specified, defaults to 85 dB(A).

    limit_value : float, optional
        Exposure limit value (in dB(A)). If not specified, defaults to 87 dB(A).

    Returns
    -------
    NoiseResult
        Object containing the computed LAeq,d exposure and flags indicating 
        whether it exceeds regulatory thresholds (action and limit values).

    Raises
    ------
    TypeError
        If `tasks` is not a list, or any element is not a dictionary.
    
    ValueError
        If required keys are missing or if input values are invalid.

    See Also
    --------
    NoiseExposure : Class used for computing LAeq,d and evaluating compliance.
    NoiseResult : Object containing the final exposure result and thresholds assessment.

    Examples
    --------
    >>> import jsapy as jsa
    >>> tasks = [
    ...     {"name": "Cutting", "laeq_t": 92, "time": 60},
    ...     {"laeq_t": 85, "time": 240}
    ... ]
    >>> result = jsa.noise_exposure(tasks)
    >>> print(result)
    85.517

    >>> jsa.display(result)
    --- Noise Exposure Result ---
    Unprotected LAeq,d: 85.52 dB(A)
    Exposure exceeds the **superior action value** of 85.0 dB(A).
    Preventive measures are needed.
    """
    
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