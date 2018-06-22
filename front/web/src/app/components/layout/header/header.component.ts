import { Component, OnInit } from '@angular/core';
import { CookieService } from "ngx-cookie-service";
import {User} from "../../../models/user";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  current_user: string;

  constructor(private cookieservice: CookieService) { }

  ngOnInit() {
    let email = this.cookieservice.get('current_user');

    this.current_user = email ? email : null;
  }

}
