import {Component, OnInit} from "@angular/core";
import {Post, Posts} from "../../../models/post";
import {Pagination} from "../../../models/pagination";
import {Board} from "../../../models/board";
import {ActivatedRoute, Router} from "@angular/router";
import {PostService} from "../../../services/post.service";
import {AuthService} from "../../../services/auth.service";
import {User} from "../../../models/user";

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {

  postList: Post[] = [];
  pagination: Pagination;
  board: Board;
  user: User;

  isOwner: boolean = false;

  constructor(private route: ActivatedRoute,
              private postService: PostService,
              private authService: AuthService,
              private router: Router) { }

  goPostDetail(post_id: number) {
    this.router.navigate([`/posts/${post_id}`]);
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let board_id = params['id'];

      this.postService.getPostList(board_id)
        .subscribe((data: Posts) => {
          this.board = data.board;
          this.postList = data.posts;
          this.pagination = data.pagination;
          this.user = data.user;

          this.isOwner = this.authService.isOwner(this.user.email);
        })
    })
  }

}
