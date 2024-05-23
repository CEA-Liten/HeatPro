from functools import reduce
from typing import Callable

from ..temporal_demand import TemporalHeatDemand

def compose(functions: list[Callable]) -> Callable:
    """Compose a list of functions into a single function.

    This function takes a list of functions and returns a new function that
    applies each function in the list sequentially.

    Args:
        functions (list[Callable]): A list of functions to be composed.

    Returns:
        Callable: A composed function that applies each function in the list.
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

def disaggregate_temporal_demand(input_aggregate_demand: TemporalHeatDemand,
                                 functions: list[Callable[[TemporalHeatDemand],TemporalHeatDemand]]) -> TemporalHeatDemand:
    """Disaggregate temporal heat demand using a list of functions.

    This function applies a list of functions to disaggregate a given
    temporal heat demand. If the list of functions is empty, the original
    demand is returned unchanged.

    Args:
        input_aggregate_demand (TemporalHeatDemand): The input aggregate demand
            to be disaggregated.
        functions (list[Callable[[TemporalHeatDemand],TemporalHeatDemand]]):
            A list of functions to be applied for disaggregation.

    Returns:
        TemporalHeatDemand: The disaggregated temporal heat demand.
    """
    if functions:
        # Compose the functions into a single function
        composed_function = compose(functions)
        
        # Apply the composed function to the input demand
        return composed_function(input_aggregate_demand)
    
    else:
        # If no functions are provided, return the input demand unchanged
        return input_aggregate_demand
