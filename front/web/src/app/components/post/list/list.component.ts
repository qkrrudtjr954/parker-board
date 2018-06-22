import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {PostService} from "../../../services/post.service";
import {Post, Posts} from "../../../models/post";
import {Pagination} from "../../../models/pagination";
import {Board} from "../../../models/board";

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  postlist: Post[] = [];
  pagination: Pagination;
  board: Board;

  constructor(private route: ActivatedRoute, private postservice: PostService) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let board_id = params['id'];

      this.postservice.getPostList(board_id)
        .subscribe((data: Posts) => {
          this.postlist = data.posts;
          this.pagination = data.pagination;
          this.board = data.board;
        })
    })
  }

}
