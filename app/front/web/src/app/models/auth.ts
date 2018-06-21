import { User } from './user';

export interface AfterLogin {
  next: string,
  user: User
}

export interface AfterLogout {
  message: string
}
