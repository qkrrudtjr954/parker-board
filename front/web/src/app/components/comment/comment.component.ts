import {Component, Input, OnChanges, OnInit} from '@angular/core';
import {CommentService} from "../../services/comment.service";


interface Comment {
  id: number;
  content: string;
  created_at: string;
  depth: number;
  step: number;
  user: {
    id: number;
    email: string;
  }
}

@Component({
  selector: 'app-comment',
  template: `
    <app-comment-form (addComment)="helloworld($event)"></app-comment-form>
    <app-comment-list [commentList]="commentList" [paginationParam]="paginationParam" [total]="total"></app-comment-list>
    <app-comment-pagination (pageChange)="pageChange($event)"></app-comment-pagination>
  `
})
export class CommentComponent implements OnChanges {
  @Input() postId: number;

  paginationParam: {page:number, per_page:number} = {
    page: 1,
    per_page: 10
  };

  commentList: Comment[];
  total: number;

  constructor(private commentService: CommentService) { }

  ngOnChanges() {
    this.getCommentList()
  }

  pageChange($event) {
    this.paginationParam.page = $event;
    this.getCommentList()
  }

  getCommentList() {
    this.commentService.getCommentList(this.postId, this.paginationParam)
      .subscribe((data: {comment_list: Comment[], total: number}) => {
        this.commentList = data.comment_list;
        this.total = data.total;
      })
  }

  helloworld($event) {
    console.log($event)
  }
}
