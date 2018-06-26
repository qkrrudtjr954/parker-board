import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {PostService} from "../../../services/post.service";
import {Post, Posts} from "../../../models/post";
import {Pagination} from "../../../models/pagination";
import {Board} from "../../../models/board";
import {AuthService} from "../../../services/auth.service";


interface Authenticate {
  result: boolean
}

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  postList: Post[] = [];
  pagination: Pagination;
  board: Board;

  isOwner: boolean = false;

  constructor(private route: ActivatedRoute, private postservice: PostService, private authservice: AuthService, private router: Router) { }

  goPostDetail(post_id: number) {
    this.router.navigate([`/posts/${post_id}`]);
  }
  ngOnInit() {
    this.route.params.subscribe(params => {
      let board_id = params['id'];

      this.authservice.isOwner(board_id)
        .subscribe((data: Authenticate) =>
          this.isOwner = data.result
        );

      this.postservice.getPostList(board_id)
        .subscribe((data: Posts) => {
          this.postList = data.posts;
          this.pagination = data.pagination;
          this.board = data.board;
        })
    })
  }

}
