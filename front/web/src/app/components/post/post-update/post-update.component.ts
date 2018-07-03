import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {Post, PostDetailData} from "../../../models/post";
import {ActivatedRoute, Router} from "@angular/router";
import {PostService} from "../../../services/post.service";

@Component({
  selector: 'app-post-update',
  templateUrl: './post-update.component.html',
  styleUrls: ['./post-update.component.css']
})
export class PostUpdateComponent implements OnInit {
  private targetPost: Post;
  updateForm = new FormGroup({
    title: new FormControl(),
    content: new FormControl()
  });

  constructor(private activatedRoute: ActivatedRoute,
              private postService: PostService,
              private fb: FormBuilder,
              private router: Router) { }

  ngOnInit() {
    this.activatedRoute.params.subscribe(params => {
      const postId = params['id'];
      this.postService.getPost(postId)
        .subscribe((data: Post) => {
          console.log(data);
          this.targetPost = data;
          this.createForm();
        })
    })
  }

  createForm() {
    this.updateForm = this.fb.group({
      title: [this.targetPost.title, [Validators.required, Validators.minLength(5)]],
      content: [this.targetPost.content, [Validators.required, Validators.minLength(20)]]
    });
  }

  confirmUpdate() {
    const title = this.updateForm.controls['title'].value;
    const content = this.updateForm.controls['content'].value;

    return this.postService.updatePost({postId: this.targetPost.id, title:title, content:content})
      .subscribe((data : { id:number }) => {
        alert('게시글이 수정 됐습니다.');
        this.router.navigate([`/posts/${data.id}`])
      })
  }

  confirmSubmit() {
    if(confirm('수정하시겠습니까?')) {
      this.confirmUpdate();
    }
  }

}
