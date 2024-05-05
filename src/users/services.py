import uuid

#from .constants import USER_ACTIVATION_UUID_NAMESPACE   #noqa
from .tasks import send_activation_mail



class Activator:
    def __init__(self, email: str) -> None:
        self.email = email
        

    def create_activation_key(self) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)


    def create_activation_link(self, activation_key: uuid.UUID) -> str:
        """Из ключа активации формирует строку - activation_link"""
        return f"https://frontend.com/users/activate/{activation_key}"


    def send_user_activation_email(self, activation_key: uuid.UUID):
        """Send activation email using SMTP"""
        
        activation_link = self.create_activation_link(activation_key)

        send_activation_mail.delay(recipient=self.email, activation_link=activation_link)  #noqa


    def save_activation_information(self, internal_user_id: int, activation_key: uuid.UUID) -> None:  #noqa
        """Save activation information to the cache.
        # 1. Connect to the cache
        # 2. Save the next structure to the cache:
        #{"activation:92d4bfa2-1f9c-447f-b4c6-6f5bd73bd75a" :{"user_id": 3}}   
        # 3. Return None
        """

        # create Redis connection instance
        # save the record to the Redis with TTL of 1 day

        raise NotImplementedError


    def validate_activation(self, activation_key: uuid.UUID):
        """Validate the activation UUID in the cache

        1. Build the key in the activation namespace:
             activation:92d4bfa2-1f9c-447f-b4c6-6f5bd73bd75a
        2. Retreive record from the cache
        3. 404 if doesn't exist of the generation TTL > 1 day
        4. 00 if exists & update user.is_active => True

        """

        # Create Redis connection instance
        # Generate the key based on the activation amespace
        # update user table. is_active = True

        raise NotImplementedError




# Function approach
# def create_activation_key(email: str) -> uuid.UUID:
#     return uuid.uuid3(namespace=uuid.uuid4(), name=email)

# def create_activation_link(activation_key: uuid.UUID) -> str:
#     """Из ключа активации формирует строку - activation_link"""
#     return f"https://frontend.com/users/activate/{activation_key}"

# def send_user_activation_email(email: str, activation_key: uuid.UUID):
#     """Send activation email using SMTP"""
    
#     activation_link = create_activation_link(activation_key)
#     send_activation_mail.delay(recipient=email, activation_link=activation_link)   #noqa


