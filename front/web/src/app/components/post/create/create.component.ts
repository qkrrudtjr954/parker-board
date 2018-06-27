import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {PostService} from "../../../services/post.service";
import {Post} from "../../../models/post";
import {ActivatedRoute, Router} from "@angular/router";
import {BoardService} from "../../../services/board.service";

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class PostCreateComponent implements OnInit {
  private boardId: number;

  makeForm = new FormGroup({
    title: new FormControl(),
    content: new FormControl()
  });

  constructor(private fb: FormBuilder,
              private router: Router,
              private postService: PostService,
              private boardService: BoardService,
              private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.createForm();

    this.activatedRoute.params.subscribe(params => {
      this.boardId = params['id'];
    })
  }

  createForm() {
    this.makeForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(5)]],
      content: ['', [Validators.required, Validators.minLength(20)]]
    });
  }


  onSubmit() {

    const title = this.makeForm.controls['title'].value;
    const content = this.makeForm.controls['content'].value;

    return this.postService.createPost({boardId: this.boardId, title:title, content:content})
      .subscribe((data : { id:number }) => {
        alert('게시글이 생성 됐습니다.');
        this.router.navigate([`/posts/${data.id}`])
      })
  }

}
