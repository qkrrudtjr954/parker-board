import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";

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

  constructor(private fb: FormBuilder, private authservice: AuthService) {
    this.createForm()
  }

  createForm() {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    })
  }

  onSubmit(){
    let email = this.loginForm.controls['email'].value;
    let password = this.loginForm.controls['password'].value;

    this.authservice.userLogin(email, password).subscribe(data => {
      console.log(data);
    })
  }

  ngOnInit() {
  }

}
