import {Component, OnInit} from "@angular/core";
import {AuthService} from "../../../services/auth.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";


@Component({
  selector: 'auth-logout',
  template: `
    <a class="nav-link" (click)="userLogout()">Sign out</a>
  `
})
export class LogoutComponent implements OnInit {
  constructor(private authservice: AuthService, private cookieservice: CookieService, private router: Router) { }

  userLogout() {
    this.authservice.userLogout()
      .subscribe(() => {
        this.cookieservice.delete('session');
        this.cookieservice.delete('current_user');
        alert('로그아웃 되었습니다.');
        this.router.navigate(['/']);
      }, error => {
        if(error.status == 401) {
          alert('로그인 후 가능합니다.');
        }
      });
  }

  ngOnInit() {
  }

}
