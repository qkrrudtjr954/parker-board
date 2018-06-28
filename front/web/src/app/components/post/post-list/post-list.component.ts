import {Component, OnInit} from "@angular/core";
import {PostList, PostListItem} from "../../../models/post";
import {ActivatedRoute, Router} from "@angular/router";
import {PostService} from "../../../services/post.service";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {
  private paginationParam: {page:number, per_page:number} = {
    page: 1,
    per_page: 10
  };

  boardId:number;
  postList: PostListItem[] = [];
  totalCount: number = 0;

  constructor(private route: ActivatedRoute,
              private postService: PostService,
              private authService: AuthService,
              private router: Router) { }


  pageChange($event) {
    this.paginationParam.page = $event;
    this.getPostList();
  }

  getPostList() {
    this.postService.getPostList(this.boardId, this.paginationParam)
        .subscribe((data: PostList) => {
          this.postList = data.posts;
          this.totalCount = data.total_count;
        })
  }

  perPageChange(event) {
    this.paginationParam.per_page = event.target.value;
    this.getPostList();
  }

  goPostDetail(post_id: number) {
    this.router.navigate([`/posts/${post_id}`]);
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.boardId = params['id'];
      this.getPostList();
    })
  }

}
