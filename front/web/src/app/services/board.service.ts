import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Board } from "../models/board";

@Injectable({
  providedIn: 'root'
})
export class BoardService {
  uri = 'http://localhost:5000'

  constructor(private http: HttpClient) { }

  getBoardList() {
    return this.http.get<Board[]>(`${this.uri}/boards`)
  }
}
