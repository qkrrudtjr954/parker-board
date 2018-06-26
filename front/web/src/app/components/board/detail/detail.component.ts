import {Component, OnInit} from "@angular/core";
import {Post, Posts} from "../../../models/post";
import {Pagination} from "../../../models/pagination";
import {Board} from "../../../models/board";
import {ActivatedRoute, Router} from "@angular/router";
import {PostService} from "../../../services/post.service";
import {AuthService} from "../../../services/auth.service";
import {CookieService} from "ngx-cookie-service";
import {User} from "../../../models/user";

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class BoardDetailComponent implements OnInit {

  postList: Post[] = [];
  pagination: Pagination;
  board: Board;
  user: User;

  isOwner: boolean = false;

  constructor(private route: ActivatedRoute,
              private postservice: PostService,
              private authservice: AuthService,
              private router: Router,
              private cookie: CookieService) { }

  goPostDetail(post_id: number) {
    this.router.navigate([`/posts/${post_id}`]);
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let board_id = params['id'];

      this.postservice.getPostList(board_id)
        .subscribe((data: Posts) => {
          this.board = data.board;
          this.postList = data.posts;
          this.pagination = data.pagination;
          this.user = data.user;

          this.isOwner = this.cookie.get('current_user') === this.user.email;
        })
    })
  }

}
