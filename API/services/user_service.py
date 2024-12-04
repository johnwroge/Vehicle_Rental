
from typing import List, Dict, Optional
from repositories.user_repository import UserRepository
from models import User

class UserService:
   def __init__(self, user_repo: UserRepository):
       self.user_repo = user_repo

   def create_user(self, user_data: dict) -> int:
       user = User(**user_data)
       return self.user_repo.create(user)

   def get_user(self, user_id: int) -> Optional[User]:
       return self.user_repo.get_by_id(user_id)

   def update_user(self, user_id: int, user_data: dict) -> bool:
       user_data['user_id'] = user_id
       user = User(**user_data)
       return self.user_repo.update(user)

   def delete_user(self, user_id: int) -> bool:
       return self.user_repo.delete(user_id)