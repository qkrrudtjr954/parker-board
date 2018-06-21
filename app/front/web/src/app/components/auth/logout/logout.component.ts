import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'auth-logout',
  template: `
    <a class="nav-link" (click)="userLogout()">Sign out</a>
  `
})
export class LogoutComponent implements OnInit {
  constructor(private authservice: AuthService) { }

  userLogout() {
    this.authservice.userLogout()
  }

  ngOnInit() {
  }

}
