import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommentService} from "../../../services/comment.service";

@Component({
  selector: 'app-comment-list',
  template: `
      <h2>comment list area</h2>
      
      <div *ngFor="let comment of commentList | paginate: { itemsPerPage: paginationParam.per_page, currentPage: paginationParam.page, totalItems: total }; index as i;">
        <div class="row">
          <div class="col-md-2">
            <span class="user_email">{{comment.user.email}}</span>
          </div>
          <div class="text-left col-md-8" [ngStyle]="{'padding-left.px': comment.depth*50}">
            <span>{{comment.content}}</span>
            <layer-comment-form [commentGroupId]="comment.comment_group_id" [parentId]="comment.id" (addLayerComment)="addLayerComment($event)"></layer-comment-form>
          </div>
          <div class="col-md-2">{{comment.created_at | date: 'yyyy-MM-dd hh:mm:ss'}}</div>
        </div>
      </div>
  `,
  styles: [`
    span.user_email{ 
      font-size: 12px;
    }
  `]
})
export class CommentListComponent implements OnInit {
  @Input() commentList;
  @Input() paginationParam;
  @Input() total;

  @Output('addLayerComment') alc = new EventEmitter();

  constructor() { }

  addLayerComment($event) {
    this.alc.emit($event);
  }

  ngOnInit() {
  }

}
