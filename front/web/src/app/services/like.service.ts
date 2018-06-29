import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class LikeService {
  uri = 'http://localhost:5000';
  options = {
    withCredentials: true
  };

  constructor(private http: HttpClient) { }

  likePost(postId: number) {
    return this.http.post(`${this.uri}/posts/${postId}/like`, {}, this.options);
  }

  unlikePost(postId: number) {
    return this.http.post(`${this.uri}/posts/${postId}/unlike`, {}, this.options);
  }

  isLiked(postId: number) {
    return this.http.get(`${this.uri}/posts/${postId}/is-liked`, this.options)

  }
}
