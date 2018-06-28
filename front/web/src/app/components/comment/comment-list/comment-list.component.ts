import {Component, Input, OnInit} from '@angular/core';
import {CommentService} from "../../../services/comment.service";
import {Comment, CommentList} from "../../../models/comment";

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.css']
})
export class CommentListComponent implements OnInit {
  @Input() postId: number;

  private paginationParam: {page:number, per_page:number} = {
    page: 1,
    per_page: 10
  };

  commentList: Comment[] = [];
  totalCount: number = 0;

  constructor(private commentService: CommentService) { }

  ngOnInit() {
    this.getCommentList();
  }

  getCommentList() {
    this.commentService.getCommentList(this.postId, this.paginationParam)
      .subscribe((data: CommentList) => {
        this.commentList = data.comment_list;
        this.totalCount = data.total_count;
        console.log(data);
      })
  }

  pageChange($event) {
    this.paginationParam.page = $event;
    this.getCommentList();
  }

  perPageChange(event) {
    this.paginationParam.per_page = event.target.value;
    console.log(this.paginationParam)
    this.getCommentList();
  }

}
