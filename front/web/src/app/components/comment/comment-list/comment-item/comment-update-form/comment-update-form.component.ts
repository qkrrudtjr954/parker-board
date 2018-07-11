import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-comment-update-form',
  template: `
    <form [formGroup]="commentUpdateForm">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="댓글을 입력해주세요" formControlName="content">
        
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" type="button" (click)="confirmSubmit()">Button</button>
        </div>
      </div>
    </form>
  `,
  styles: []
})
export class CommentUpdateFormComponent implements OnInit {
  @Output() updateComment = new EventEmitter();

  @Input() defaultValue: string = '';

  commentUpdateForm = new FormGroup({
    content: new FormControl()
  });

  constructor(private fb: FormBuilder) {
  }

  private createForm() {
    this.commentUpdateForm = this.fb.group({
      content: [this.defaultValue, [Validators.required, Validators.minLength(5)]]
    })
  }

  ngOnInit() {
    this.createForm();
  }

  confirmSubmit() {
    let contentControl = this.commentUpdateForm.controls['content'];

    if (contentControl.invalid) {
      alert('내용은 5글자 이상 입력해주세요.');
      return;
    }

    if(confirm('댓글을 수정하시겠습니까?')) {
      this.updateComment.emit(contentControl.value);
    }
  }

}
