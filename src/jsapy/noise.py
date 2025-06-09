import numpy as np
import math
import warnings
from typing import Optional

class NoiseResult:
    """
    Class to represent the result of a noise exposure assessment.

    Attributes
    ----------
    exposure_value : float
        Unprotected equivalent continuous sound level (LAeq,d) in dB(A).
    with_hearing_protection : bool
        Indicates whether hearing protection was used during exposure.
    protected_exposure_value : float or None
        Equivalent exposure value when using hearing protection, if available. NOT WORK
    inf_action_value : float
        Inferior action value threshold defined by regulations.
    sup_action_value : float
        Superior action value threshold defined by regulations.
    limit_value : float
        Limit value threshold defined by regulations.
    exceeds_inf_action : bool
        True if the exposure exceeds the inferior action value.
    exceeds_sup_action : bool
        True if the exposure exceeds the superior action value.
    exceeds_limit : bool
        True if the exposure exceeds the limit value.
    """
    
    def __init__(self, exposure_value: float, inf_action_value: float, sup_action_value: float, limit_value: float, with_hearing_protection: bool = False, protected_laeq_d: Optional[float] = None):
        """
        Initialize a NoiseResult object.

        Parameters
        ----------
        exposure_value : float
            Measured unprotected LAeq,d value in dB(A).
        inf_action_value : float
            Inferior action value threshold in dB(A).
        sup_action_value : float
            Superior action value threshold in dB(A).
        limit_value : float
            Exposure limit value in dB(A).
        with_hearing_protection : bool, optional
            Whether hearing protection is considered, by default False. NOT WORK
        protected_laeq_d : float, optional
            LAeq,d value when using hearing protection, if applicable.
        """
        
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
        """
        Return a string representation of the unprotected exposure value.

        Returns
        -------
        str
            Rounded string of the LAeq,d value without protection.
        """
        return str(np.round(self.exposure_value, 3))

    def to_dict(self):
        """
        Convert the NoiseResult object to a dictionary.

        Returns
        -------
        dict
            Dictionary containing all relevant attributes of the assessment.
        """
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
        """
        Generate a detailed textual summary of the noise assessment.

        Returns
        -------
        str
            Human-readable summary of the LAeq,d value and its regulatory status.
            Includes whether hearing protection was used and whether exposure exceeds
            action or limit thresholds, along with suggested actions.
        """
        
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
    """
    Class for assessing daily noise exposure levels (LAeq,d).

    Provides methods to calculate normalized daily exposure from
    a single measurement or to compute the total exposure from
    multiple sources.

    Attributes
    ----------
    inf_action_value : float
        Lower action value threshold in dB(A). Default is 80.0.
    sup_action_value : float
        Upper action value threshold in dB(A). Default is 85.0.
    limit_value : float
        Limit value threshold in dB(A). Default is 87.0.
    """
    
    def __init__(self, inf_action_value=None, sup_action_value=None, limit_value=None):
        """
        Initialize a NoiseExposure object with regulatory thresholds.

        Parameters
        ----------
        inf_action_value : float, optional
            Lower action value threshold in dB(A). Defaults to 80.0.
        sup_action_value : float, optional
            Upper action value threshold in dB(A). Defaults to 85.0.
        limit_value : float, optional
            Limit value threshold in dB(A). Defaults to 87.0.
        """
        
        self.inf_action_value = inf_action_value if inf_action_value is not None else 80.0
        self.sup_action_value = sup_action_value if sup_action_value is not None else 85.0
        self.limit_value = limit_value if limit_value is not None else 87.0
        
    def _validate_inputs(self, id, laeq_t, exposure_time_minutes):
        """
        Validate input parameters for noise exposure calculations.

        Parameters
        ----------
        id : str
            Identifier for the measurement or task.
        laeq_t : float
            Measured equivalent continuous sound level (LAeq,T) in dB(A).
        exposure_time_minutes : float
            Duration of exposure in minutes.

        Raises
        ------
        TypeError
            If input types are not numeric.
        ValueError
            If values are non-positive.
        UserWarning
            If exposure time exceeds 8 hours (480 minutes).
        """
        
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
        """
        Calculate the normalized daily noise exposure (LAeq,d).

        Parameters
        ----------
        id : str
            Identifier for the task or tool.
        laeq_t : float
            Measured LAeq,T in dB(A).
        exposure_time_minutes : float
            Duration of exposure in minutes.

        Returns
        -------
        float
            Normalized daily exposure level (LAeq,d) in dB(A).

        Raises
        ------
        ValueError
            If input validation fails.
        """
        
        self._validate_inputs(id, laeq_t, exposure_time_minutes)
        
        laeq_d = laeq_t + 10*math.log10(exposure_time_minutes/480)
        
        return laeq_d
    
    def calculate_total(self, list_of_exposure):
        """
        Calculate the total LAeq,d from multiple exposure events.

        Parameters
        ----------
        list_of_exposure : array_like
            Sequence of individual LAeq,d values in dB(A).

        Returns
        -------
        NoiseResult
            Object containing the combined LAeq,d value and regulatory assessment.

        Raises
        ------
        ValueError
            If input contains invalid or non-numeric values.
        """
        
        list_of_exposure = np.atleast_1d(list_of_exposure)
        
        laeq_d = 10 * math.log10(np.sum(10**(list_of_exposure/10)))
        
        return NoiseResult(
            exposure_value = laeq_d, 
            inf_action_value = self.inf_action_value, 
            sup_action_value = self.sup_action_value,
            limit_value = self.limit_value
            )