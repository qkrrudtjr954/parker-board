import {User} from "./user";
import {Pagination} from "./pagination";
import {Comment} from "./comment";

export interface PostList {
  total_count: number;
  post_list: PostListItem[];
}

export interface PostListItem {
  id: number;
  title: string;
  comments_count: number;
  read_count: number;
  created_at: string;
  user: User;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  like_count: number;
  read_count: number;
  created_at: string;
  updated_at: string;
  comments_count: number;
  user: User;
}

export interface PostDetailData {
  comments: Comment[];
  pagination: Pagination;
  post: Post;
  user: User;
}

