import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-comment-delete',
  template: `
    <a (click)="deleteComment()"> 삭제 </a>
  `,
  styles: [`
    a {
      font-size: 15px;
    }
  `]
})
export class CommentDeleteComponent implements OnInit {
  @Input() commentId: number;
  @Input() userEmail: string;

  @Output('deleteComment') del = new EventEmitter<number>();
  constructor() { }

  deleteComment() {
    if(confirm('정말 삭제하시겠습니까?')) {
      this.del.emit(this.commentId);
    }
  }

  ngOnInit() {
  }

}
