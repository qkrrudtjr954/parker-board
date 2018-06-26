import { Component, OnInit } from '@angular/core';
import { CookieService } from "ngx-cookie-service";
import {User} from "../../../models/user";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  currentUser: string;

  constructor(private cookieservice: CookieService) { }

  setCurrentUserEamil(){
    let email = this.cookieservice.get('current_user');
    this.currentUser = email ? email : null;
  }

  ngOnInit() {
    this.setCurrentUserEamil();
  }

}
