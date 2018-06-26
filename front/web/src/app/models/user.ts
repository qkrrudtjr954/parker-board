export interface User {
  id: number,
  email: string
}


export interface RegistUser {
  email: string;
  password: string;
}


export interface AfterRegisterUser {
  email: string;
  created_at: string;
}
