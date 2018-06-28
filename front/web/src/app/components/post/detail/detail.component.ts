import { Component, OnInit } from '@angular/core';
import {Post, PostDetailData} from "../../../models/post";
import {PostService} from "../../../services/post.service";
import {ActivatedRoute} from "@angular/router";
import {Comment} from "../../../models/comment";
import {Pagination} from "../../../models/pagination";
import {AuthService} from "../../../services/auth.service";
import {User} from "../../../models/user";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class PostDetailComponent implements OnInit {
  isOwner: boolean;
  post: Post;
  comments: Comment[];
  pagination: Pagination;
  user: User;


  constructor(private route: ActivatedRoute,
              private postService: PostService,
              private authService: AuthService,
              private fb: FormBuilder) { }


  getPost(post_id: number) {
    return this.postService.getPost(post_id)
      .subscribe((data: PostDetailData) => {
        this.post = data.post;
        this.comments = data.comments;
        this.pagination = data.pagination;
        this.user = data.user;
        this.isOwner = this.authService.isOwner(this.user.email);
      })
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let post_id = params['id'];
      this.getPost(post_id);
    })
  }

}
