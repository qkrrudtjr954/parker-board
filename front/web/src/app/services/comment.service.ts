import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  uri = 'http://localhost:5000';
  options = {
    withCredentials: true
  };

  constructor(private http: HttpClient) { }

  createComment(content: string) {

  }

  getCommentList(postId: number, paginationParam: {page: number, per_page: number}) {
    let paginationUri = `?page=${paginationParam.page}&per_page=${paginationParam.per_page}`;
    return this.http.get(`${this.uri}/posts/${postId}/comments${paginationUri}`, this.options)
  }
}
