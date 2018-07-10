import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-comment-list',
  template: `
      <h2>comment list area</h2>
      
      <div *ngFor="let comment of commentList | paginate: { itemsPerPage: paginationParam.per_page, currentPage: paginationParam.page, totalItems: total }; index as i;">
        <div class="row">
          <div class="col-md-3">
            <span class="user_email">{{comment.user.email}}</span>
          </div>
          <div class="text-left col-md-7" [ngStyle]="{'padding-left.px': comment.depth*20}">
            <span>{{comment.content}}</span>
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

  constructor() { }

  ngOnInit() {
  }

}
