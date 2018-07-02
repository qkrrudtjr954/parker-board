import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {AfterRegisterUser} from "../../../models/user";
import {Router} from "@angular/router";


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  signUpForm = new FormGroup({
    email: new FormControl(),
    password: new FormControl(),
    passwordConfirm: new FormControl(),
  });

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) { }

  createForm() {
    this.signUpForm = this.fb.group({
      email: ['', [Validators.email, Validators.required]],
      passwordGroup: this.fb.group({
        password: ['', [Validators.minLength(6), Validators.required]],
        confirmPassword: ['', [Validators.minLength(6), Validators.required]]
      }, { validator : CustomValidator.passwordMather })
    })
  }

  ngOnInit() {
    this.createForm();
  }

  resetForm() {
    this.signUpForm.reset();
  }

  onSubmit() {
    const emailControl = this.signUpForm.controls['email'];
    const passwordGroup = this.signUpForm.get('passwordGroup')

    this.authService.userRegister({email: emailControl.value, password: passwordGroup.get('password').value})
      .subscribe((data: AfterRegisterUser)=> {
        alert(data.email +' 님 가입을 축하드립니다.');
        // this.router.navigate([`login`]);
        location.href='/login';

      }, error1 => {
        if (error1.status == 400) {
          alert('이미 존재하는 이메일 입니다.');
        } else if (error1.status == 500) {
          alert('서버에 에러가 발생했습니다. 다시 시도해주세요.');
        } else if (error1.status == 422) {
          alert('입력값을 다시 확인해주세요.');
        }

        passwordGroup.get('password').setValue('');
        passwordGroup.get('confirmPassword').setValue('');
      });
  }

}

class CustomValidator {
  static passwordMather(control: AbstractControl): {[key: string]: boolean} {
    const pwd1 = control.get('password');
    const pwd2 = control.get('confirmPassword');

    if (pwd1 == null || pwd2 == null) return { invalid: true };
    return (pwd1.value === pwd2.value) ? null : { nomatch: true, invalid: false };
  };
}
