import numpy as np
import math
import warnings

class VibraResult:
    """
    Class to represent the result of a vibration exposure assessment.
    
    Attributes
    ----------
    exposure_value : float
        Measured vibration exposure value (A(8)).
    exposure_type : str
        Type of exposure, either "hand-arm" or "body".
    action_value : float
        Action value threshold defined by regulations.
    limit_value : float
        Limit value threshold defined by regulations.
    unit : str, optional
        Unit of measurement, default is "m/s²".
    exceeds_action : bool
        True if the exposure exceeds the action value.
    exceeds_limit : bool
        True if the exposure exceeds the limit value.
    """
    
    def __init__(self, exposure_value: float, exposure_type: str, action_value: float, limit_value: float, unit: str = "m/s²"):
        """
        Initialize a VibraResult object.

        Parameters
        ----------
        exposure_value : float
            Measured vibration exposure value (A(8)).
        exposure_type : str
            Type of exposure ("hand-arm" or "body").
        action_value : float
            Regulatory threshold for action.
        limit_value : float
            Regulatory threshold for limit.
        unit : str, optional
            Unit of measurement, default is "m/s²".
        """

        self.exposure_value = exposure_value
        self.exposure_type = exposure_type
        self.action_value = action_value
        self.limit_value = limit_value
        self.unit = unit

        self.exceeds_action = exposure_value > action_value
        self.exceeds_limit = exposure_value > limit_value

    def __str__(self):
        """
        Return a string representation of the exposure value.

        Returns
        -------
        str
            Rounded string representation of the exposure value.
        """
        
        return str(np.round(self.exposure_value, 3))
    
    def to_display(self):
        """
        Generate a detailed textual summary of the vibration assessment.

        Returns
        -------
        str
            Human-readable summary of the exposure value and its implications.
            Indicates whether the exposure exceeds regulatory thresholds and 
            suggests corresponding actions.
        """
        
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
        """
        Convert the VibraResult object to a dictionary.

        Returns
        -------
        dict
            Dictionary containing all relevant attributes of the assessment.
        """
        
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
    """
    Class for evaluating hand-arm vibration exposure.

    This class provides methods to compute the A(8) vibration exposure value
    based on either a single vector magnitude or the combination of three
    orthogonal axes (ax, ay, az), as well as a method to compute the total
    combined exposure from multiple sources.

    Attributes
    ----------
    action_value : float
        Action threshold value for vibration exposure in m/s².
        Default is 2.5 m/s².
    limit_value : float
        Limit threshold value for vibration exposure in m/s².
        Default is 5 m/s².
    unit : str
        Unit of measurement for vibration values. Default is "m/s²".
    """
    
    def __init__(self, action_value=None, limit_value=None, unit=None):
        """
        Initialize a HandArmVibrations object.

        Parameters
        ----------
        action_value : float, optional
            Action value threshold. Defaults to 2.5 if not provided.
        limit_value : float, optional
            Limit value threshold. Defaults to 5 if not provided.
        unit : str, optional
            Unit of measurement. Defaults to "m/s²".
        """
        self.action_value = action_value if action_value is not None else 2.5
        self.limit_value = limit_value if limit_value is not None else 5
        self.unit = unit if unit is not None else "m/s²"
        
    def _validate_inputs(self, id, aw, ax, ay, az, exposure_time_hours):
        """
        Validate input parameters for vibration calculation.

        Ensures the proper combination of inputs is used (either `aw` or
        the components `ax`, `ay`, and `az`), that all values are numeric
        and non-negative, and that exposure time is within acceptable bounds.

        Parameters
        ----------
        id : str
            Identifier for the measurement or equipment.
        aw : float or None
            Pre-computed total vibration magnitude.
        ax : float or None
            Vibration component in the x-axis.
        ay : float or None
            Vibration component in the y-axis.
        az : float or None
            Vibration component in the z-axis.
        exposure_time_hours : float
            Duration of exposure in hours.

        Raises
        ------
        ValueError
            If input values are missing, negative, or inconsistent.
        TypeError
            If numeric values are not of type int or float.
        UserWarning
            If exposure time exceeds 8 hours.
        """
            
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
        """
        Compute the vector magnitude `aw` if not directly provided.

        Parameters
        ----------
        aw : float or None
            Pre-computed magnitude.
        ax : float
            Vibration component on the x-axis.
        ay : float
            Vibration component on the y-axis.
        az : float
            Vibration component on the z-axis.

        Returns
        -------
        float
            Computed or provided value of `aw`.
        """
        if aw is not None:
            return aw
        return math.sqrt(ax**2 + ay**2 + az**2)
    
    def _compute_a8(self, aw, exposure_time_hours):
        """
        Compute the A(8) vibration exposure value.

        Parameters
        ----------
        aw : float
            Total vibration value (m/s²).
        exposure_time_hours : float
            Duration of exposure in hours.

        Returns
        -------
        float
            A(8) vibration exposure value.
        """
        return aw * math.sqrt(exposure_time_hours / 8)
    
    def calculate_a8(self, id, ax=None, ay=None, az=None, aw=None, exposure_time_hours=None):
        """
        Calculate the A(8) vibration exposure based on input data.

        Parameters
        ----------
        id : str
            Identifier for the measurement or equipment.
        ax : float, optional
            Vibration component on the x-axis.
        ay : float, optional
            Vibration component on the y-axis.
        az : float, optional
            Vibration component on the z-axis.
        aw : float, optional
            Pre-computed total vibration value.
        exposure_time_hours : float
            Duration of exposure in hours.

        Returns
        -------
        float
            A(8) vibration exposure value.

        Raises
        ------
        ValueError
            If inputs are invalid or inconsistent.
        """
        self._validate_inputs(id, aw, ax, ay, az, exposure_time_hours)
        aw = self._compute_aw(aw, ax, ay, az)
        a8 = self._compute_a8(aw, exposure_time_hours)
        
        return a8
        
    def calculate_total(self, list_of_exposure):
        """
        Calculate the total A(8) exposure from multiple sources.

        Parameters
        ----------
        list_of_exposure : array_like
            Sequence of individual A(8) values to be combined.

        Returns
        -------
        VibraResult
            Object containing the total A(8) value and assessment results.

        Raises
        ------
        ValueError
            If input array contains invalid values.
        """
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
    """
    Class for evaluating whole-body vibration exposure.

    This class provides methods to calculate the A(8) vibration values for 
    complete-body exposure based on acceleration measurements along the 
    x, y, and z axes. The x and y axes are weighted with a factor of 1.4 
    as required by international standards.

    Attributes
    ----------
    action_value : float
        Action threshold value for whole-body vibration exposure in m/s².
        Default is 0.5 m/s².
    limit_value : float
        Limit threshold value for whole-body vibration exposure in m/s².
        Default is 1.15 m/s².
    unit : str
        Unit of measurement for vibration values. Default is "m/s²".
    """
    
    def __init__(self, action_value=None, limit_value=None, unit=None):
        """
        Initialize a CompleteBodyVibrations object.

        Parameters
        ----------
        action_value : float, optional
            Action value threshold. Defaults to 0.5 if not provided.
        limit_value : float, optional
            Limit value threshold. Defaults to 1.15 if not provided.
        unit : str, optional
            Unit of measurement. Defaults to "m/s²".
        """
        
        self.action_value = action_value if action_value is not None else 0.5
        self.limit_value = limit_value if limit_value is not None else 1.15
        self.unit = unit if unit is not None else "m/s²"
    
    def _validate_inputs(self, id, ax, ay, az, exposure_time_hours):
        """
        Validate input parameters for whole-body vibration calculation.

        Ensures that acceleration values for all three axes are provided, 
        numeric, and non-negative, and that exposure time is within bounds.

        Parameters
        ----------
        id : str
            Identifier for the measurement or equipment.
        ax : float
            Vibration component on the x-axis.
        ay : float
            Vibration component on the y-axis.
        az : float
            Vibration component on the z-axis.
        exposure_time_hours : float
            Duration of exposure in hours.

        Raises
        ------
        ValueError
            If any axis is missing or contains negative values, or if
            exposure time is not positive.
        TypeError
            If axis values are not numeric.
        UserWarning
            If exposure time exceeds 8 hours.
        """
        
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
        """
        Calculate the weighted A(8) values for each axis.

        Applies a 1.4 weighting factor to x and y axes as per ISO standards,
        and computes the A(8) equivalent values for each axis separately.

        Parameters
        ----------
        id : str
            Identifier for the measurement or equipment.
        ax : float
            Vibration component on the x-axis.
        ay : float
            Vibration component on the y-axis.
        az : float
            Vibration component on the z-axis.
        exposure_time_hours : float
            Duration of exposure in hours.

        Returns
        -------
        tuple of float
            A_x, A_y, and A_z values after applying time and axis corrections.
        """
        self._validate_inputs(id, ax, ay, az, exposure_time_hours)
        Ax = 1.4*ax*math.sqrt(exposure_time_hours/8)
        Ay = 1.4*ay*math.sqrt(exposure_time_hours/8)
        Az = az*math.sqrt(exposure_time_hours/8)
        
        return Ax, Ay, Az
    
    def calculate_total(self, exposure_x, exposure_y, exposure_z):
        """
        Calculate the total whole-body vibration A(8) value.

        Computes the root-sum-of-squares for each axis over multiple 
        exposures and returns the maximum among them as the final A(8) value.

        Parameters
        ----------
        exposure_x : array_like
            Sequence of weighted x-axis exposure values (A_x).
        exposure_y : array_like
            Sequence of weighted y-axis exposure values (A_y).
        exposure_z : array_like
            Sequence of weighted z-axis exposure values (A_z).

        Returns
        -------
        VibraResult
            Object containing the final A(8) value and assessment metadata.
        """
        
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
    