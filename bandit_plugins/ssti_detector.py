from bandit.core.test_properties import *  # Bandit plugin support
from bandit.core import issue
import ast

@takes_config
@checks('Call')
def detect_ssti(context):
    """
    Detects unsafe usage of Jinja2 Template rendering with user input.
    """
    if (isinstance(context.call_function_name_qual, str) and 
        context.call_function_name_qual.endswith('Template')):

        # Check if user input is passed into Template()
        for arg in context.node.args:
            if isinstance(arg, ast.Name):  # Variable (could be user input)
                return issue.Issue(
                    severity=issue.HIGH,
                    confidence=issue.MEDIUM,
                    text="🚨 Possible SSTI detected: User input is passed to Jinja2 Template()!"
                )

# Register plugin
def register(linter):
    linter.register_function(detect_ssti)
