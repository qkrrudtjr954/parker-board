import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Post, PostDetailData, Posts} from "../models/post";

@Injectable({
  providedIn: 'root'
})
export class PostService {
  uri = 'http://localhost:5000';
  options = {
    withCredentials: true
  };

  constructor(private http: HttpClient) { }

  getPostList(board_id: number) {
    return this.http.get<Posts>(`${this.uri}/boards/${board_id}/posts`, this.options)
  }

  getPost(post_id: number) {
    return this.http.get<PostDetailData>(`${this.uri}/posts/${post_id}`, this.options)
  }

  createPost(param) {
    return this.http.post(`${this.uri}/boards/${param.boardId}/posts`, param, this.options);
  }

  updatePost(param: { postId: number; title: string; content: string }) {
    return this.http.patch(`${this.uri}/posts/${param.postId}`, param, this.options);
  }
}
