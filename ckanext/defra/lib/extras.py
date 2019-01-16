# Helper functions for working with extras


def unwrap_value_list(value):
    if isinstance(value, list):
        if value:
            return value[0]
        return None
        
    return value