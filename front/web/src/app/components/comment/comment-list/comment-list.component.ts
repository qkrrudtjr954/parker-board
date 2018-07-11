import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommentService} from "../../../services/comment.service";

@Component({
  selector: 'app-comment-list',
  template: `
      <div class="comment_container">
        <div *ngFor="let comment of commentList | paginate: { itemsPerPage: paginationParam.per_page, currentPage: paginationParam.page, totalItems: total }; index as i;"  [ngStyle]="{'padding-left.px': comment.depth*50}">
          <app-comment-item (addLayerComment)="addLayerComment($event)" [comment]="comment"></app-comment-item>
        </div>
      </div>
  `,
  styles: [`
    
    div.comment_container {
      background: whitesmoke;
      padding: 10px;
    }
    div.comment_container > div {
      border-bottom: 2px solid gray;
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
