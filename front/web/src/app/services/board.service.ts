import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Board } from "../models/board";
import {Observable} from "rxjs/internal/Observable";


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
    return this.http.get<Board[]>(`${this.uri}/boards`);
  }

  makeBoard(board: Board): Observable<Board> {
    let data = {
      title: board.title,
      description: board.description
    };

    return this.http.post<Board>(`${this.uri}/boards`, data, this.options);
  }

  updateBoard(board_id: number, title: string, description: string) {
    let data = {
      title: title,
      description: description
    };

    return this.http.patch(`${this.uri}/boards/${board_id}`, data, this.options)
  }
}
