import { User } from "./user";
import {Pagination} from "./pagination";

export interface Board {
  id: number,
  title: string,
  description: string,
  user: User
}

export interface Boards {
  pagination: Pagination,
  boards: Board[]
}
