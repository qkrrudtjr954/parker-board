import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  uri = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  options = {
    withCredentials: true
  };

  userLogin(email, password) {
    let login_data = {
      email: email,
      password: password
    };

    return this.http.post(`${this.uri}/users/login`, login_data, this.options);
  }

  userLogout() {
    return this.http.get(`${this.uri}/users/logout`, this.options);
  }
}
