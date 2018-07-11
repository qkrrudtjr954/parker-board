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

  addComment(postId: number, content: string) {
    return this.http.post(`${this.uri}/posts/${postId}/comments`, {content: content}, this.options)
  }

  addLayerComment(data) {
    return this.http.post(`${this.uri}/comment_groups/${data.commentGroupId}/comments`, {content: data.content, parent_id: data.parentId}, this.options)
  }

  getCommentList(postId: number, paginationParam: {page: number, per_page: number}) {
    let paginationUri = `?page=${paginationParam.page}&per_page=${paginationParam.per_page}`;
    return this.http.get(`${this.uri}/posts/${postId}/comments${paginationUri}`, this.options)
  }

  deleteComment(commentId: number) {
    return this.http.delete(`${this.uri}/comments/${commentId}`, this.options);
  }
}
