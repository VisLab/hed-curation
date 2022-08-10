

class BaseOp:

    def __init__(self, command, required_params, optional_params):
        if command:
            self.command = command
        else:
            raise ValueError("OpMustHaveCommand", "BaseOp command is empty")
        self.required_params = required_params
        self.optional_params = optional_params

    def check_parameters(self, parameters):
        # Check for required arguments
        required = set(self.required_params.keys())
        required_missing = required.difference(set(parameters.keys()))
        if required_missing:
            raise KeyError("MissingRequiredParameters", f"{self.command} requires parameters {list(required_missing)}")
        for param_name, param_value in parameters.items():
            if param_name in self.required_params:
                param_type = self.required_params[param_name]
            elif param_name in self.optional_params:
                param_type = self.optional_params[param_name]
            else:
                raise KeyError("BadParameter", f"{param_name} not a required or optional parameter for {self.command}")
            if isinstance(param_type, list):
                self._check_list_type(param_value, param_type)
            elif not isinstance(param_value, param_type):
                raise TypeError("BadType" f"{param_value} has type {type(param_value)} not {param_type}")

    def do_op(self, df, hed_schema=None, sidecar=None):
        return df

    def _check_list_type(self, param_value, param_type):
        for type in param_type:
            if isinstance(param_value, type):
                return
        raise TypeError("BadType" f"{param_value} has type {type(param_value)} which is not in {str(param_type)}")
