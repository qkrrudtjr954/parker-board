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

  getCommentList(postId: number) {
    return this.http.get(`/posts/${postId}/comments`, this.options)
  }
}
