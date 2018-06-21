import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BoardService {
  uri = 'http://localhost:5000'

  constructor(private http: HttpClient) { }

  getBoardList(per_page, page) {
    const pagination_param = {
      params: {
        page: page,
        per_page: per_page
      }
    };

    return this.http.get(`${this.uri}/boards`, pagination_param)
  }
}
