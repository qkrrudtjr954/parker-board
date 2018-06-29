import {Component, OnInit} from '@angular/core';
import { CookieService } from "ngx-cookie-service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  currentUser: string;

  constructor(private cookieService: CookieService) { }

  setCurrentUserEamil(){
    let email = this.cookieService.get('current_user');
    this.currentUser = email ? email : null;
  }

  ngOnInit() {
    this.setCurrentUserEamil();
  }

}
