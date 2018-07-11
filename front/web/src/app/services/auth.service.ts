import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import {RegistUser} from "../models/user";


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  uri = 'http://localhost:5000';
  currentUser: string;

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
    this.currentUser = null;
    return this.http.get(`${this.uri}/users/logout`, this.options);
  }

  userRegister(user: RegistUser) {
    return this.http.post(`${this.uri}/users/`, user, this.options);
  }

  getCurrentUserInfo() {
    return this.http.get(`${this.uri}/users/user-info`, this.options)
  }
}
