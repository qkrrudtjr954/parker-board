import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommentService} from "../../../services/comment.service";

@Component({
  selector: 'app-comment-list',
  template: `
      <div class="comment_container">
        <div *ngFor="let comment of commentList | paginate: { itemsPerPage: paginationParam.per_page, currentPage: paginationParam.page, totalItems: total }; index as i;"  [ngStyle]="{'padding-left.px': comment.depth*50}">
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
            <i-corner-down-right></i-corner-down-right>
            <span>
              {{comment.content}}
            </span>
            <layer-comment-form [commentGroupId]="comment.comment_group_id" [parentId]="comment.id" (addLayerComment)="addLayerComment($event)"></layer-comment-form>
          </div>
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
    div.comment_container {
      background: ;
      padding: 10px;
    }
    div.comment_container > div {
      border-bottom: 2px solid gray;
    }
    div.comment_content {
      padding-bottom: 15px;
    }
  `]
})
export class CommentListComponent implements OnInit {
  isShowUpdateForm: boolean = false;

  @Input() commentList;
  @Input() paginationParam;
  @Input() total;

  @Output('addLayerComment') alc = new EventEmitter();
  @Output('deleteComment') dc = new EventEmitter();

  constructor() { }

  addLayerComment($event) {
    this.alc.emit($event);
  }

  deleteComment($event) {
    this.dc.emit($event);
  }

  showButton(email) {
    return localStorage.getItem('user_info') === email;
  }

  ngOnInit() {
  }

}
