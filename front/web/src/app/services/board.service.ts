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

  updateBoard(updateBoard: Board) {
    return this.http.patch(`${this.uri}/boards/${updateBoard.id}`, updateBoard, this.options)
  }

  getBoard(boardId: number) {
    return this.http.get<Board>(`${this.uri}/boards/${boardId}`);
  }
}
