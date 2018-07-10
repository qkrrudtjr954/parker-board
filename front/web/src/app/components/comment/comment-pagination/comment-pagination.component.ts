import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-comment-pagination',
  template: `
    <div class="d-flex justify-content-center">
      <pagination-controls (pageChange)="pageChange($event)"></pagination-controls>
    </div>
  `
})
export class CommentPaginationComponent implements OnInit {
  @Output('pageChange') pageChanger = new EventEmitter<number>();
  constructor() { }

  ngOnInit() {
  }

  pageChange($event) {
    this.pageChanger.emit($event);
  }
}
