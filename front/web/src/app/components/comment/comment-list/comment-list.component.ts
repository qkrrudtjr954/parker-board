import {Component, Input, OnInit} from '@angular/core';
import {CommentService} from "../../../services/comment.service";
import {Comment} from "../../../models/comment";

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

  constructor(private commentService: CommentService) { }

  ngOnInit() {
    this.commentService.getCommentList(this.postId)
      .subscribe((data: Comment[]) => {
        console.log('comment list')
      })
  }

  pageChange($event) {
    this.paginationParam.page = $event;

  }

}
