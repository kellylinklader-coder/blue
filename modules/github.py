import requests
import re
from logger import Logger

class GitHubScanner:
    """GitHub user and email enumeration"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def get_users(self, comp, target):
        """Extract GitHub users from organization"""
        users = []
        
        try:
            self.logger.info(f"Searching GitHub users for {comp}")
            gitpeople = f"https://github.com/orgs/{comp}/people"
            response = requests.get(gitpeople)
            
            if response.status_code == 200:
                listusers = re.findall(r'self" href="[a-zA-Z0-9\-/]{3,}', response.text)
                
                for item in listusers:
                    x = re.sub(r'self" href="/', "", item)
                    users.append(x)
                
                users_set = set(users)
                for idx, user in enumerate(users_set, 1):
                    user_url = f"https://github.com/{user}"
                    self.logger.success(f"{idx}. {user_url}")
                
                self.logger.info(f"Found {len(users_set)} GitHub users")
                return list(users_set)
        except Exception as e:
            self.logger.error(f"GitHub user scan error: {str(e)}")
        
        return users
    
    def harvest_emails(self, target, users):
        """Harvest emails from GitHub users and DuckDuckGo"""
        emails = []
        
        try:
            self.logger.info(f"Harvesting emails for {target}")
            
            # From GitHub user events
            for user in users:
                try:
                    userpage = f"https://api.github.com/users/{user}/events/public"
                    response = requests.get(userpage)
                    findemail = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', response.text)
                    
                    for email in findemail:
                        if target in email and email not in emails:
                            emails.append(email)
                            self.logger.success(f"Email: {email}")
                except:
                    pass
            
            # From DuckDuckGo
            try:
                searchurl = f'https://duckduckgo.com/html/?q=site%3Alinkedin.com+email+%40%22{target}%22'
                response = requests.get(searchurl)
                findem = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', response.text)
                
                for email in findem:
                    if target in email and email not in emails:
                        emails.append(email)
                        self.logger.success(f"Email: {email}")
            except:
                pass
            
            self.logger.info(f"Found {len(emails)} emails")
        except Exception as e:
            self.logger.error(f"Email harvesting error: {str(e)}")
        
        return emails
