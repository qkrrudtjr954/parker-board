import {User} from "./user";
import {Board} from "./board";
import {Pagination} from "./pagination";
import {Comment} from "./comment";

export interface Posts {
  board: Board;
  pagination: Pagination;
  posts: Post[];
}

export interface PostDetailData {
  comments: Comment[];
  pagination: Pagination;
  post: Post;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  comments_count: number;
  user: User;
}
