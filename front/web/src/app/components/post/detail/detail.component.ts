import { Component, OnInit } from '@angular/core';
import {Post, PostDetailData } from "../../../models/post";
import {PostService} from "../../../services/post.service";
import {ActivatedRoute} from "@angular/router";
import {Comment} from "../../../models/comment";
import {Pagination} from "../../../models/pagination";
import {AuthService} from "../../../services/auth.service";
import {User} from "../../../models/user";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {CommentService} from "../../../services/comment.service";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class PostDetailComponent implements OnInit {
  postId: number;

  private paginationParam: {page:number, per_page:number} = {
    page: 1,
    per_page: 10
  };

  post: Post;
  comments: Comment[];
  pagination: Pagination;
  user: User;

  isOwner: boolean;

  constructor(private route: ActivatedRoute,
              private postService: PostService,
              private commentService: CommentService,
              private authService: AuthService,
              private fb: FormBuilder) { }


  getPost(postId: number) {
    this.postId = postId;

    return this.postService.getPost(postId, this.paginationParam)
      .subscribe((data: PostDetailData) => {
        this.post = data.post;
        this.user = data.user;
        this.comments = data.comments;
        this.pagination = data.pagination;

        this.isOwner = this.authService.isOwner(this.user.email);
      })
  }

  pageChange($event) {
    this.paginationParam.page = $event;
    this.getPost(this.postId);
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let post_id = params['id'];
      this.getPost(post_id);
    })
  }

}
