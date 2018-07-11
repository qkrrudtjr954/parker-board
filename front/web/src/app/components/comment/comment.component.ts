import {Component, Input, OnInit } from '@angular/core';
import {CommentService} from "../../services/comment.service";


interface Comment {
  id: number;
  content: string;
  created_at: string;
  comment_group_id: number;
  parent_id: number;
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
    <div class="row">
      <div class="offset-md-2 col-md-8">
        <app-comment-form (addComment)="addComment($event)"></app-comment-form>
      </div>
    </div>
    <div class="row">
      <div class="offset-md-2 col-md-8">
        <app-comment-list [commentList]="commentList" [paginationParam]="paginationParam" [total]="total" 
                          (addLayerComment)="addLayerComment($event)"></app-comment-list>
      </div>
    </div>
    <app-pagination (pageChange)="pageChange($event)"></app-pagination>
  `
})
export class CommentComponent implements OnInit {
  @Input() postId: number;

  paginationParam: {page:number, per_page:number} = {
    page: 1,
    per_page: 10
  };

  commentList: Comment[];
  total: number;

  constructor(private commentService: CommentService) { }

  ngOnInit() {
    this.getCommentList();
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

  addComment($event) {
    this.commentService.addComment(this.postId, $event)
      .subscribe((data) => {
        this.paginationParam.page=1;
        this.getCommentList();
      }, error1 => {
        if (error1.status == 422) {
          alert('입력값에 오류가 있습니다. 다시 확인하고 시도해주세요.');
        } else {
          alert('문제가 발생했습니다. 다시 시도해주세요.')
        }
      })
  }

  addLayerComment($event) {
    this.commentService.addLayerComment($event)
      .subscribe((data) => {
        this.getCommentList();
      }, error1 => {
        if (error1.status == 422) {
          alert('입력값에 오류가 있습니다. 다시 확인하고 시도해주세요.');
        } else {
          alert('문제가 발생했습니다. 다시 시도해주세요.')
        }
      })
  }



}
