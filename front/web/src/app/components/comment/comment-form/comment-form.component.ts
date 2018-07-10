import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-comment-form',
  template: `
    <form [formGroup]="commentForm">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Recipient's username" formControlName="content">
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" type="button" (click)="confirmSubmit()">Button</button>
        </div>
      </div>
    </form>
  `,
})
export class CommentFormComponent implements OnInit {
  @Output() addComment = new EventEmitter<string>();

  commentForm = new FormGroup({
    content: new FormControl()
  });

  constructor(private fb: FormBuilder) {
    this.createForm()
  }

  private createForm() {
    this.commentForm = this.fb.group({
      content: ['', Validators.required ],
    })
  }

  ngOnInit() {
  }

  confirmSubmit() {
    if(confirm('댓글을 등록하시겠습니까?')) {
      this.addComment.emit(this.commentForm.controls['content'].value);
    }
  }
}
