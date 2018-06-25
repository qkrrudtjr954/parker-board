import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http';
import {CookieService} from "ngx-cookie-service";


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  uri = 'http://localhost:5000';
  constructor(private http: HttpClient, private cookie: CookieService) { }

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

  isOwner(target_id: number) {
    return this.http.get(`${this.uri}/boards/${target_id}/owner`, this.options)
  }

  isLoggedIn() {
    return this.http.get(`${this.uri}/users/authenticate`, this.options)
  }
}
