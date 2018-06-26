import { Component, OnInit } from '@angular/core';
import {Post, PostDetailData} from "../../../models/post";
import {PostService} from "../../../services/post.service";
import {ActivatedRoute} from "@angular/router";
import {Comment} from "../../../models/comment";
import {Pagination} from "../../../models/pagination";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class PostDetailComponent implements OnInit {
  post: Post;
  comments: Comment[];
  pagination: Pagination;

  constructor(private route: ActivatedRoute, private postService: PostService) { }

  getPost(post_id: number) {
    return this.postService.getPost(post_id)
      .subscribe((data: PostDetailData) => {
        console.log(data);
        this.post = data.post;
        this.comments = data.comments;
        this.pagination = data.pagination;
      })
  }
  ngOnInit() {
    this.route.params.subscribe(params => {
      let post_id = params['id'];

      this.getPost(post_id);
    })
  }

}
