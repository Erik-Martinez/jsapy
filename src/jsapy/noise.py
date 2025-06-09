import numpy as np
import math
import warnings
from typing import Optional

class NoiseResult:
    """
    Represents the daily noise exposure result.

    Attributes
    ----------
     exposure_value : float
        Daily noise exposure level (in dB(A)).
    with_hearing_protection : bool
        Whether hearing protection is used.
    protected_laeq_d : Optional[float]
        LAeq,d after applying hearing protection attenuation.
    action_value : float
        Regulatory action threshold, default is 80 dB(A).
    limit_value : float
        Regulatory limit threshold, default is 85 dB(A).
    exceeds_action : bool
        Whether the action threshold is exceeded.
    exceeds_limit : bool
        Whether the limit threshold is exceeded.
    """
    
    def __init__(self, exposure_value: float, inf_action_value: float, sup_action_value: float, limit_value: float, with_hearing_protection: bool = False, protected_laeq_d: Optional[float] = None):
        self.exposure_value =  exposure_value
        self.with_hearing_protection = with_hearing_protection
        self.protected_exposure_value = protected_laeq_d
        
        self.inf_action_value = inf_action_value
        self.sup_action_value = sup_action_value
        self.limit_value = limit_value

        # Choose which LAeq,d to compare
        self._comparison_value = protected_laeq_d if protected_laeq_d else exposure_value
        
        self.exceeds_inf_action = self._comparison_value >= self.inf_action_value
        self.exceeds_sup_action = self._comparison_value >= self.sup_action_value
        self.exceeds_limit = self._comparison_value >= self.limit_value

    def __str__(self):
        return str(np.round(self.exposure_value, 3))

    def to_dict(self):
        return {
            "exposure_value": self.exposure_value,
            "protected_exposure_value": self.protected_exposure_value,
            "with_hearing_protection": self.with_hearing_protection,
            "inf_action_value": self.inf_action_value,
            "sup_action_value": self.sup_action_value,
            "limit_value": self.limit_value,
            "exceeds_inf_action": self.exceeds_inf_action,
            "exceeds_sup_action": self.exceeds_sup_action,
            "exceeds_limit": self.exceeds_limit
        }

    def to_display(self):
        lines = ["--- Noise Exposure Result ---"]
        lines.append(f"Unprotected LAeq,d: {self.exposure_value:.2f} dB(A)")
        if self.with_hearing_protection and self.protected_exposure_value:
            lines.append(f"Protected LAeq,d: {self.exposure_value:.2f} dB(A)")
        #value = self.protected_exposure_value if self.with_hearing_protection else self.laeq_d
        if self.exceeds_limit:
            lines.append(f"Exposure exceeds the **limit value** of {self.limit_value:.1f} dB(A).")
            lines.append("Immediate action is required.")
        elif self.exceeds_sup_action:
            lines.append(f"Exposure exceeds the **superior action value** of {self.sup_action_value:.1f} dB(A).")
            lines.append("Preventive measures are needed.")
        elif self.exceeds_inf_action:
            lines.append(f"Exposure exceeds the **Inferior action value** of {self.inf_action_value:.1f} dB(A). ")
            lines.append("Preventive measures are needed.")
        else:
            lines.append("Exposure is within acceptable regulatory thresholds.")
        return "\n".join(lines)
    
    
class NoiseExposure:
    
    def __init__(self, inf_action_value=None, sup_action_value=None, limit_value=None):
        self.inf_action_value = inf_action_value if inf_action_value is not None else 80.0
        self.sup_action_value = sup_action_value if sup_action_value is not None else 85.0
        self.limit_value = limit_value if limit_value is not None else 87.0
        
    def _validate_inputs(self, id, laeq_t, exposure_time_minutes):
        if not isinstance(laeq_t, (int, float)):
            raise TypeError(f"{id}: LAeq,T must be a numeric value (int or float).")
        if not isinstance(exposure_time_minutes, (int, float)):
            raise TypeError(f"{id}: Exposure time must be a numeric value (int or float).")

        if laeq_t <= 0:
            raise ValueError(f"{id}: LAeq,T must be greater than zero.")
        if exposure_time_minutes <= 0:
            raise ValueError(f"{id}: Exposure time must be greater than zero.")
        
        if exposure_time_minutes > 480:
            warnings.warn(f"{id}- Exposure time exceeds 8 hours.", UserWarning)
            
    def calculate_laeq_d(self, id, laeq_t, exposure_time_minutes):
        self._validate_inputs(id, laeq_t, exposure_time_minutes)
        
        laeq_d = laeq_t + 10*math.log10(exposure_time_minutes/480)
        
        return laeq_d
    
    def calculate_total(self, list_of_exposure):
        list_of_exposure = np.atleast_1d(list_of_exposure)
        
        laeq_d = 10 * math.log10(np.sum(10**(list_of_exposure/10)))
        
        return NoiseResult(
            exposure_value = laeq_d, 
            inf_action_value = self.inf_action_value, 
            sup_action_value = self.sup_action_value,
            limit_value = self.limit_value
            )