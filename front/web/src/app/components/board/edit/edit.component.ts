import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {BoardService} from "../../../services/board.service";
import {ActivatedRoute} from "@angular/router";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {
  editForm = new FormGroup({
    title: new FormControl(),
    description: new FormControl()
  });

  constructor(private fb: FormBuilder,
              private boardservice: BoardService,
              private router: Router,
              private activerouter: ActivatedRoute) {

    this.createForm()
  }

  createForm() {
    this.editForm = this.fb.group({
      title: ['', Validators.minLength(10)],
      description: []
    })
  }

  onSubmit() {
    let title = this.editForm.controls['title'].value;
    let description = this.editForm.controls['description'].value;

    this.activerouter.params.subscribe(params => {
      let board_id = params['id'];

      return this.boardservice.updateBoard(board_id, title, description)
        .subscribe((data) => {
          console.log(data);
          alert('수정되었습니다.');
        }, error1 => {
          console.log(error1)

          if (error1.status == 401 && error1.error == 'No Authentication.') {
            alert('본인만 수정 가능합니다.');
          }else if (error1. status == 401 && error1.error != 'Login first.'){
            alert('로그인해주세요.');
            this.router.navigate(['login'])
          } else if (error1.status == 422) {
            alert('입력값을 확인해주세요.');
          } else if (error1.status == 500) {
            alert('서버 에러가 발생했습니다. 다시 시도해주세요.');
          }
        })
    });
  }

  ngOnInit() {

  }

}
