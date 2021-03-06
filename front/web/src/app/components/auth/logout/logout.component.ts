import {Component, OnInit} from "@angular/core";
import {AuthService} from "../../../services/auth.service";
import {CookieService} from "ngx-cookie-service";


@Component({
  selector: 'auth-logout',
  template: `
    <a class="nav-link" (click)="userLogout()">Sign out</a>
  `
})
export class LogoutComponent implements OnInit {
  constructor(private authService: AuthService) { }

  userLogout() {
    this.authService.userLogout()
      .subscribe((data) => {
        localStorage.removeItem('user_info');
        alert('로그아웃 되었습니다.');
        location.href = '/';
      }, error => {
        if(error.status == 401) {
          alert('로그인 후 가능합니다.');
        }
      });
  }

  ngOnInit() {
  }

}
