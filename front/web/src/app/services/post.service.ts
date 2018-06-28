import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Post, PostDetailData, PostList } from "../models/post";

@Injectable({
  providedIn: 'root'
})
export class PostService {
  uri = 'http://localhost:5000';
  options = {
    withCredentials: true
  };

  constructor(private http: HttpClient) { }

  getPostList(board_id: number, paginationParam: {page: number, per_page: number}) {
    let paginationUri = `?page=${paginationParam.page}&per_page=${paginationParam.per_page}`;

    return this.http.get<PostList>(`${this.uri}/boards/${board_id}/posts${paginationUri}`, this.options)
  }

  getPost(post_id: number, paginationParam: {page: number, per_page: number}) {
    let paginationUri = `?page=${paginationParam.page}&per_page=${paginationParam.per_page}`;
    return this.http.get<PostDetailData>(`${this.uri}/posts/${post_id}${paginationUri}`, this.options)
  }

  createPost(param) {
    return this.http.post(`${this.uri}/boards/${param.boardId}/posts`, param, this.options);
  }

  updatePost(param: { postId: number; title: string; content: string }) {
    return this.http.patch(`${this.uri}/posts/${param.postId}`, param, this.options);
  }
}
