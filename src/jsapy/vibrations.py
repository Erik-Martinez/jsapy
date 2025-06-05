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

    def __str__(self):
        
        return str(np.round(self.exposure_value, 3))
    
    def to_display(self):
        
        if self.exposure_type == "hand-arm":
            text = [
                "--- Hand-Arm Vibration Exposure Assessment ---"
            ]
            
        elif self.exposure_type == "body":
            text = [
                "--- Complete Body Vibration Exposure Assessment ---"
            ]
                  
        text.append(f"A(8) vibration value: {self.exposure_value:.3f} {self.unit}.")
        
        if self.exceeds_limit == True:
            text.append(f"Danger: Exposure exceeds the **Exposure Limit Value ({self.limit_value}{self.unit})**.")
            text.append("Immediate action is required to reduce vibration levels.")
        elif self.exceeds_action == True:
            text.append(f"Danger: Exposure exceeds the **Exposure Action Value ({self.limit_value}{self.unit})**.")
            text.append("Preventive measures should be implemented to control exposure.")
        else:
            text.append("Exposure is below the action value.")
            text.append("No specific action is required.")          
            
        return "\n".join(text)
    
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
    


class HandArmVibrations:
    
    def __init__(self, action_value=None, limit_value=None, unit=None):
        self.action_value = action_value if action_value is not None else 2.5
        self.limit_value = limit_value if limit_value is not None else 5
        self.unit = unit if unit is not None else "m/s²"
        
    def _validate_inputs(self, id, aw, ax, ay, az, exposure_time_hours):
            
        if aw is not None and any(v is not None for v in [ax, ay, az]):
            raise ValueError(f"{id}- Must be provided either 'aw' or 'ax, ay, az', not both.")
        
        if aw is None:
            for val, name in zip([ax, ay, az], ['ax', 'ay', 'az']):
                if val is None:
                    raise ValueError(f"{id}- Missing required axis value: '{name}'")
                if not isinstance(val, (int, float)):
                    raise TypeError(f"{id}- '{name}' must be numeric.")
                if val < 0:
                    raise ValueError(f"{id}-'{name}' must be non-negative.")
        else:
            if not isinstance(aw, (int, float)):
                raise TypeError(f"{id}-'aw' must be numeric.")
            if aw < 0:
                raise ValueError(f"{id}- 'aw' must be numeric.")
        
        if 0 >= exposure_time_hours:
            raise ValueError(f"{id}-  Exposure time must be non-negative.")
        
        if exposure_time_hours > 8:
            warnings.warn(f"{id}- Exposure time exceeds 8 hours.", UserWarning)
                  
    def _compute_aw(self, aw, ax, ay, az):
        if aw is not None:
            return aw
        return math.sqrt(ax**2 + ay**2 + az**2)
    
    def _compute_a8(self, aw, exposure_time_hours):
        return aw * math.sqrt(exposure_time_hours / 8)
    
    def calculate_a8(self, id, ax=None, ay=None, az=None, aw=None, exposure_time_hours=None):
        self._validate_inputs(id, aw, ax, ay, az, exposure_time_hours)
        aw = self._compute_aw(aw, ax, ay, az)
        a8 = self._compute_a8(aw, exposure_time_hours)
        
        return a8
        
    def calculate_total(self, list_of_exposure):
        list_of_exposure = np.atleast_1d(list_of_exposure)
        
        a8 = math.sqrt(np.sum(list_of_exposure**2))
        
        return VibraResult(
            exposure_value = a8,
            exposure_type = "hand-arm",
            action_value = self.action_value,
            limit_value = self.limit_value,
            unit = self.unit
            )
        

class CompleteBodyVibrations:
    
    def __init__(self, action_value=None, limit_value=None, unit=None):
        self.action_value = action_value if action_value is not None else 0.5
        self.limit_value = limit_value if limit_value is not None else 1.15
        self.unit = unit if unit is not None else "m/s²"
    
    def _validate_inputs(self, id, ax, ay, az, exposure_time_hours):
        
        for val, name in zip([ax, ay, az], ['ax', 'ay', 'az']):
            if val is None:
                raise ValueError(f"{id}- Missing required axis value: '{name}'")
            if not isinstance(val, (int, float)):
                    raise TypeError(f"{id}- '{name}' must be numeric.")
            if val < 0:
                    raise ValueError(f"{id}-'{name}' must be non-negative.")
        
        if 0 >= exposure_time_hours:
            raise ValueError(f"{id}-  Exposure time must be non-negative.")
        
        if exposure_time_hours > 8:
            warnings.warn(f"{id}- Exposure time exceeds 8 hours.", UserWarning)
            
    def calculate_A_vertex(self, id, ax, ay, az, exposure_time_hours):
        self._validate_inputs(id, ax, ay, az, exposure_time_hours)
        Ax = 1.4*ax*math.sqrt(exposure_time_hours/8)
        Ay = 1.4*ay*math.sqrt(exposure_time_hours/8)
        Az = az*math.sqrt(exposure_time_hours/8)
        
        return Ax, Ay, Az
    
    def calculate_total(self, exposure_x, exposure_y, exposure_z):
        exposure_x = np.atleast_1d(exposure_x)
        exposure_y = np.atleast_1d(exposure_y)
        exposure_z = np.atleast_1d(exposure_z)
    
        A_x = math.sqrt(np.sum(exposure_x**2))
        A_y = math.sqrt(np.sum(exposure_y**2))
        A_z = math.sqrt(np.sum(exposure_z**2))
        
        A8 = max([A_x, A_y, A_z])
        
        return VibraResult(
            exposure_value = A8,
            exposure_type= "body",
            action_value = self.action_value,
            limit_value = self.limit_value,
            unit = self.unit
        )
    