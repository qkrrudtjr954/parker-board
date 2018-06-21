import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  uri = 'http://localhost:5000'
  constructor(private http: HttpClient) { }

  header= new HttpHeaders({
    'Content-Type': 'application/json'
  });

  options = {
    withCredentials: true,
    headers: this.header
  };

  userLogin(email, password) {
    let login_data = {
      email: email,
      password: password
    };

    return this.http.post(`${this.uri}/users/login`, login_data, this.options);
  }

  userLogout() {
    return this.http.delete(`${this.uri}/users/logout`, this.options);

  }
}
