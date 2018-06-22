import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Board } from "../models/board";

@Injectable({
  providedIn: 'root'
})
export class BoardService {
  uri = 'http://localhost:5000'
  options = {
    withCredentials: true
  };

  constructor(private http: HttpClient) { }

  getBoardList() {
    return this.http.get<Board[]>(`${this.uri}/boards`)
  }

  makeBoard(title: string, description: string) {
    let data = {
      title: title,
      description: description
    };

    return this.http.post(`${this.uri}/boards`, data, this.options)
  }
}
