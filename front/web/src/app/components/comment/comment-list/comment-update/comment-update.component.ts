import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-comment-update',
  template: `
    <a (click)="updateComment()"> 수정 </a>
  `,
  styles: [`
    a {
      font-size: 15px;
    }
  `]
})
export class CommentUpdateComponent implements OnInit {
  @Input() commentId: number;

  @Output('updateComment') uc = new EventEmitter();
  constructor() { }

  updateComment() {
    this.uc.emit(this.commentId);
  }
  ngOnInit() {
  }

}
