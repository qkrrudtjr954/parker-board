import { Component, OnInit } from '@angular/core';
import {Post, PostDetailData } from "../../../models/post";
import {PostService} from "../../../services/post.service";
import {ActivatedRoute} from "@angular/router";
import {AuthService} from "../../../services/auth.service";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {CommentService} from "../../../services/comment.service";
import {LikeService} from "../../../services/like.service";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})

export class PostDetailComponent implements OnInit {
  postId: number;
  post: Post;

  isOwner: boolean;
  isLiked: boolean = false;

  constructor(private route: ActivatedRoute,
              private postService: PostService,
              private commentService: CommentService,
              private authService: AuthService,
              private likeService: LikeService) { }


  getPost(postId: number) {
    this.postId = postId;

    this.postService.getPost(postId)
      .subscribe((data: Post) => {
        this.post = data;
        this.isOwner = this.authService.isOwner(this.post.user.email);
      })
  }

  likePost($event) {
    if($event) {
      this.likeService.likePost(this.postId)
        .subscribe((data: {like_count: number}) => {
          this.post.like_count = data.like_count;
          this.isLiked = true;
        })
    } else {
      this.likeService.unlikePost(this.postId)
        .subscribe((data: {like_count: number}) => {
          this.post.like_count = data.like_count;
          this.isLiked = false;
        })
    }
  }

  setIsLiked() {
    this.likeService.isLiked(this.postId)
      .subscribe((data: {is_liked: boolean}) => {
        this.isLiked = data.is_liked;
      })
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let post_id = params['id'];
      this.getPost(post_id);
      this.setIsLiked();
    })
  }

}
