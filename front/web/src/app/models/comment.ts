import {User} from "./user";

export interface Comment {
  id: number;
  content: string;
  user: User;
  created_at: string;
}


export interface CommentList {
  comment_list: Comment[];
  total_count: number;
}
