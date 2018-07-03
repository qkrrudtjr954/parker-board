import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, FormBuilder, Validators} from "@angular/forms";
import {BoardService} from "../../../services/board.service";
import {Router} from "@angular/router";
import {Board} from "../../../models/board";


@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class BoardCreateComponent implements OnInit {
  makeForm = new FormGroup({
    title: new FormControl(),
    description: new FormControl()
  });

  constructor(private fb: FormBuilder,
              private boardService: BoardService,
              private router: Router) { }

  createForm() {
    this.makeForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(4)]],
      description: ['']
    })
  }

  confirmSubmit() {
    let title = this.makeForm.controls['title'].value;
    let description = this.makeForm.controls['description'].value;

    return this.boardService.makeBoard({title, description} as Board)
      .subscribe((data: Board) => {
        this.router.navigate([`/boards/${data.id}/posts`]);
      }, error1 => {
        if(error1.status == 401){
          alert('로그인해주세요.');
          this.router.navigate(['login'])
        } else if (error1.status == 422){
          alert('입력값을 확인해주세요.');
        } else if (error1.status == 500){
          alert('서버 에러가 발생했습니다. 다시 시도해주세요.');
        }
      })
  }

  confirmCreate() {
    if(confirm('생성하시겠습니까?')) {
      this.confirmSubmit();
    }
  }


  ngOnInit() {
    this.createForm()
  }

}
