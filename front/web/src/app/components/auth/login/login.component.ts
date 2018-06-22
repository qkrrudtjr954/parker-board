import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {AfterLogin} from "../../../models/auth";
import { CookieService } from "ngx-cookie-service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm = new FormGroup({
    email: new FormControl(),
    password: new FormControl()
  });

  constructor(private fb: FormBuilder, private authservice: AuthService, private cookieservice: CookieService) {
    this.createForm()
  }

  createForm() {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    })
  }

  onSubmit() {
    let email = this.loginForm.controls['email'].value;
    let password = this.loginForm.controls['password'].value;

    this.authservice.userLogin(email, password)
      .subscribe((data: AfterLogin) => {
        alert(data.user.email + ' 님 환영합니다.');
        this.cookieservice.set('current_user', data.user.email);
        location.href = '/';

      }, error1 => {
        if (error1.status == 400) {
          alert('회원 정보가 존재하지 않습니다.');
        } else if (error1.status == 500) {
          alert('서버에 에러가 발생했습니다. 다시 시도해주세요.');
        } else if (error1.status == 422) {
          alert('정보를 다시 입력해주세요.');
        }
      });
  }

  ngOnInit() {
  }

}
