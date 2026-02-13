"""
Input handling utilities for Riventide
"""

from colorama import Fore, Style

def get_input(prompt, validator=None, error_message=None):
    """
    Get input from the user with validation.
    
    Args:
        prompt (str): The prompt to display to the user.
        validator (callable, optional): A function that takes the input and returns True if valid.
        error_message (str, optional): Message to display if validation fails.
        
    Returns:
        str: The validated user input.
    """
    while True:
        user_input = input(prompt)
        
        if validator is None or validator(user_input):
            return user_input
        
        if error_message:
            print(Fore.RED + error_message + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)
            
def get_choice(prompt, options, allow_back=True):
    """
    Get a choice from a list of options.
    
    Args:
        prompt (str): The prompt to display to the user.
        options (list): List of options to choose from.
        allow_back (bool): Whether to allow a "back" option.
        
    Returns:
        int: The index of the chosen option, or -1 if back was chosen.
    """
    while True:
        print("\n" + prompt + "\n")
        
        for i, option in enumerate(options, 1):
            print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {option}")
            
        if allow_back:
            print(f"{Fore.GREEN}{len(options) + 1}.{Style.RESET_ALL} Back")
            
        max_choice = len(options) + 1 if allow_back else len(options)
        
        choice = get_input(f"\nEnter your choice (1-{max_choice}): ", 
                          validator=lambda x: x.isdigit() and 1 <= int(x) <= max_choice)
                          
        choice = int(choice)
        
        if choice <= len(options):
            return choice - 1  # Return 0-based index
        else:
            return -1  # Back option
            
def confirm(prompt):
    """
    Ask for confirmation (yes/no).
    
    Args:
        prompt (str): The prompt to display to the user.
        
    Returns:
        bool: True if confirmed, False otherwise.
    """
    response = get_input(f"{prompt} (y/n): ", 
                        validator=lambda x: x.lower() in ['y', 'n', 'yes', 'no'])
                        
    return response.lower() in ['y', 'yes'] 