import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  currentUser: string;

  constructor(private authService: AuthService) { }

  setCurrentUserEmail(){
    this.authService.getCurrentUserInfo()
      .subscribe((data: {email:string}) => {
        this.currentUser = data.email;
      }, error1 => {
        console.log('error')
      })
  }

  ngOnInit() {
    this.setCurrentUserEmail();

  }

}
