import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {AfterLogin} from "../../../models/auth";
import { CookieService } from "ngx-cookie-service";
import {Router} from "@angular/router";

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

  constructor(private fb: FormBuilder,
              private authService: AuthService,
              private cookieService: CookieService,
              private router: Router) { }

  createForm() {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.minLength(6), Validators.required]]
    })
  }


  onSubmit() {
    let email = this.loginForm.controls['email'].value;
    let password = this.loginForm.controls['password'].value;

    this.authService.userLogin(email, password)
      .subscribe((data: AfterLogin) => {
        this.cookieService.set('current_user', data.user.email);

        alert(data.user.email + ' 님 환영합니다.');

        // this.router.navigate(['/']);
        location.href='/';

      }, error1 => {
        if (error1.status == 400) {
          alert('회원 정보가 존재하지 않습니다.');
        } else if (error1.status == 500) {
          alert('서버에 에러가 발생했습니다. 다시 시도해주세요.');
        } else if (error1.status == 422) {
          alert('정보를 다시 입력해주세요.');
        }

        this.loginForm.controls['password'].setValue('');
      });
  }

  ngOnInit() {
    this.createForm()
  }

}
