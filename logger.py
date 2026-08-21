import time

class Logger:
    """Simple logging utility"""
    
    # ANSI color codes
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    RED = '\033[91m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, verbose=True):
        self.verbose = verbose
    
    def info(self, message):
        """Log info message"""
        if self.verbose:
            print(f"{self.BLUE}[*]{self.RESET} {message}")
    
    def success(self, message):
        """Log success message"""
        if self.verbose:
            print(f"{self.GREEN}[+]{self.RESET} {self.BLUE}{message}{self.RESET}")
    
    def error(self, message):
        """Log error message"""
        print(f"{self.RED}[!]{self.RESET} {self.BOLD}{message}{self.RESET}")
    
    def warning(self, message):
        """Log warning message"""
        print(f"{self.YELLOW}[!]{self.RESET} {message}")
    
    def section(self, title):
        """Log section header"""
        if self.verbose:
            print(f"\n{self.BLUE}{'»' * 60}\n{self.BOLD}{title}{self.RESET}\n{'»' * 60}{self.RESET}")
