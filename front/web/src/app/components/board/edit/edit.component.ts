import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {BoardService} from "../../../services/board.service";
import {ActivatedRoute} from "@angular/router";
import {Board} from "../../../models/board";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {
  targetBoard: Board;

  editForm = new FormGroup({
    title: new FormControl(),
    description: new FormControl()
  });

  constructor(private fb: FormBuilder,
              private boardservice: BoardService,
              private router: Router,
              private activerouter: ActivatedRoute) { }

  createForm() {
    this.editForm = this.fb.group({
      title: [this.targetBoard.title, Validators.minLength(4)],
      description: [this.targetBoard.description]
    })
  }

  onSubmit() {
    const boardId = this.targetBoard.id;
    const title = this.editForm.controls['title'].value;
    const description = this.editForm.controls['description'].value;


    return this.boardservice.updateBoard({id:boardId, title:title, description:description} as Board)
      .subscribe((data) => {
        alert('수정되었습니다.');
        this.router.navigate([`/boards/${boardId}/posts`]);
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
      });
  }

  goBoardDetail() {
    this.router.navigate([`/boards/${this.targetBoard.id}/posts`])
  }

  ngOnInit() {
    this.activerouter.params.subscribe(params => {
      const boardId = params['id'];

      this.boardservice.getBoard(boardId)
        .subscribe((data:Board) => {
          this.targetBoard = data;
          this.createForm()
        }, error1 => {
          if (error1.status == 404) {
            alert('존재하지 않는 게시판입니다.');
            this.router.navigate([`/`])
          }
        });
    })
  }
}
