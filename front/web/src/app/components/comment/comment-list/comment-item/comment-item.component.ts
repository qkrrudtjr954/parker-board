import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommentService} from "../../../../services/comment.service";

@Component({
  selector: 'app-comment-item',
  template: `
    <div class="d-flex justify-content-between">

      <div class="comment_info">
        <span>{{comment.user.email}}</span>
        <span>{{comment.created_at | date: 'yyyy-MM-dd hh:mm:ss'}}</span>
      </div>
        
      <div *ngIf="showButton(comment.user.email)">
        <a (click)="isShowUpdateForm=!isShowUpdateForm">수정</a>
        <app-comment-delete [commentId]="comment.id" [userEmail]="comment.user.email" (deleteComment)="deleteComment($event)"></app-comment-delete>
      </div>
    </div>
    <div class="comment_content">
      <div *ngIf="!isShowUpdateForm">
        <i-corner-down-right></i-corner-down-right>
        <span>
          {{comment.content}}
        </span>
        <layer-comment-form [commentGroupId]="comment.comment_group_id" [parentId]="comment.id" (addLayerComment)="addLayerComment($event)"></layer-comment-form>
      </div>
      <div *ngIf="isShowUpdateForm">
        <app-comment-update-form (updateComment)="updateComment($event)" [defaultValue]="comment.content"></app-comment-update-form>
      </div>
    </div>
  `,
  styles: [`
    div.comment_info span:nth-child(1){
      font-size: 20px;
      font-weight: bold;
    }
    div.comment_info span:nth-child(2){
      margin-left: 10px;
      font-size: 10px;
    }
    div.comment_content {
      padding-bottom: 15px;
    }
  `]
})
export class CommentItemComponent implements OnInit {
  isShowUpdateForm: boolean = false;

  @Input() comment;
  @Output('addLayerComment') alc = new EventEmitter();

  constructor(private commentService: CommentService) { }

  ngOnInit() {
  }

  showButton(email) {
    return localStorage.getItem('user_info') === email && this.comment.content != '삭제된 댓글입니다.';
  }

  addLayerComment($event) {
    this.alc.emit($event);
  }

  deleteComment($event) {
    console.log('deleteComment id: ' + $event);
    this.commentService.deleteComment($event)
      .subscribe((data) => {
        this.comment.content = '삭제된 댓글입니다.'
        alert('삭제되었습니다.')
      }, error1 => {
        if (error1.status == 500) {
          alert('문제가 발생했습니다. 다시 시도해주세요.')
        } else if(error1.status == 401) {
          alert('삭제할 수 없습니다.');
        }
      })
  }

  updateComment($event) {
    let data = {
      id: this.comment.id,
      content: $event
    };

    this.commentService.updateComment(data)
      .subscribe((result) => {
        this.comment.content = data.content;
        alert('댓글이 수정되었습니다.');
        this.isShowUpdateForm = false;
      }, error1 => {
        if(error1.status == 401) {
          alert('수정할 수 없습니다.');
        } else if (error1.status == 500) {
          alert('문제가 발생했습니다. 다시 시도해주세요.')
        }
      })
  }
}
