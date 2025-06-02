import numpy as np
import math
import warnings

class VibraResult:
    
    def __init__(self, exposure_value: float, exposure_type: str, action_value: float, limit_value: float, unit: str = "m/s²"):

        self.exposure_value = exposure_value
        self.exposure_type = exposure_type
        self.action_value = action_value
        self.limit_value = limit_value
        self.unit = unit

        self.exceeds_action = exposure_value > action_value
        self.exceeds_limit = exposure_value > limit_value

    def to_dict(self):
        return {
            "exposure_value": self.exposure_value,
            "exposure_type": self.exposure_type,
            "unit": self.unit,
            "action_value": self.action_value,
            "limit_value": self.limit_value,
            "exceeds_action": self.exceeds_action,
            "exceeds_limit": self.exceeds_limit,
        }

    def __str__(self):
        
        return str(np.round(self.exposure_value, 3))
    



class HandArmVibrations:
    
    def __init__(self, action_value=2.5 , limit_value=5, unit="m/s²"):
        self.action_value = action_value
        self.limit_value = limit_value
        self.unit = unit
        
    def _validate_inputs(self, id, aw, ax, ay, az, exposure_time_hours):
            
        if aw is not None and any(v is not None for v in [ax, ay, az]):
            raise ValueError(f"{id}: Must be provided either 'aw' or 'ax, ay, az', not both.")
        
        
        if aw is None:
            for val, name in zip([ax, ay, az], ['ax', 'ay', 'az']):
                if val is None:
                    raise ValueError(f"{id}: Missing required axis value: '{name}'")
                if not isinstance(val, (int, float)):
                    raise TypeError(f"{id}: '{name}' must be numeric.")
                if val < 0:
                    raise ValueError(f"{id}:'{name}' must be non-negative.")
        else:
            if not isinstance(aw, (int, float)):
                raise TypeError(f"{id}:'aw' must be numeric.")
            if aw < 0:
                raise ValueError(f"{id}: 'aw' must be numeric.")
        
        
        if 0 >= exposure_time_hours:
            raise ValueError(f"{id}: Exposure time must be non-negative.")
        
        if exposure_time_hours > 8:
            warnings.warn(f"{id}:Exposure time exceeds 8 hours.", UserWarning)
            
        
    def _compute_aw(self, aw, ax, ay, az):
        if aw is not None:
            return aw_input
        return math.sqrt(ax**2 + ay**2 + az**2)
    
    def _compute_a8(self, aw, exposure_time_hours):
        return aw * math.sqrt(exposure_time_hours / 8)
    
    def calculate(self, id, ax=None, ay=None, az=None, aw=None, exposure_time_hours=None):
        self._validate_inputs(id, aw, ax, ay, az, exposure_time_hours)
        aw = self._compute_aw(aw, ax, ay, az)
        a8 = self._compute_a8(aw, exposure_time_hours)
        
        return VibraResult(
            exposure_value = a8,
            exposure_type = "hand-arm",
            action_value = self.action_value,
            limit_value = self.limit_value,
            unit = self.unit
            )
        
    
                