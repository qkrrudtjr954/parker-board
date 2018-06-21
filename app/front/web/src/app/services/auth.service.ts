import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs/internal/observable/throwError";


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  uri = 'http://localhost:5000'
  constructor(private http: HttpClient) { }

  options = {
    withCredentials: true
  };

  userLogin(email, password) {
    let login_data = {
      email: email,
      password: password
    };

    this.http.post(`${this.uri}/users/login`, login_data)
      .subscribe(data => {
        console.log(data);
      }, error1 => {
        console.log(error1);
      });
  }

  userLogout() {
    return this.http.get(`${this.uri}/users/logout`, this.options)
      .subscribe(data => {
        console.log(data);
      }, error => {
        console.log(error);
      });
  }
}
