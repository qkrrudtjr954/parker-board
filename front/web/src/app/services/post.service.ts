import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Posts} from "../models/post";

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
}