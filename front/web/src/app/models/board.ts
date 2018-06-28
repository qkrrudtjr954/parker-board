import { User } from "./user";
import {Pagination} from "./pagination";


//navbar 에 표시되는 board
export interface NavBoard {
  id: number,
  title: string
}

export interface Board {
  id: number,
  title: string,
  description: string,
  created_at: string,
  updated_at: string,
  user: User
}
