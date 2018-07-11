import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'layer-comment-form',
  template: `
    <a (click)="isShow=!isShow" ><span>댓글 달기</span></a>
    
    <form [formGroup]="layerCommentForm"  *ngIf="isShow">
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="댓글을 입력해주세요" formControlName="content">
        
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" type="button" (click)="confirmSubmit()">Button</button>
        </div>
      </div>
    </form>`,
  styles: [` 
    a span { 
      color: gray;
      text-decoration: none; 
      font-size: 10px;
      margin-left: 30px;
    }
  `]
})
export class LayerCommentFormComponent implements OnInit {
  isShow: boolean = false;
  @Input('commentGroupId') cgi: number;
  @Input('parentId') pi: number;

  @Output() addLayerComment = new EventEmitter();

  layerCommentForm = new FormGroup({
    content: new FormControl()
  });

  constructor(private fb: FormBuilder) {
    this.createForm()
  }

  private createForm() {
    this.layerCommentForm = this.fb.group({
      content: ['', [Validators.required, Validators.minLength(5)] ]
    })
  }

  ngOnInit() {
  }

  confirmSubmit() {
    if (this.layerCommentForm.invalid) {
      alert('내용은 5글자 이상 입력해주세요.');
      return;
    }

    if(confirm('댓글을 등록하시겠습니까?')) {
      let data = {
        'content' : this.layerCommentForm.controls['content'].value,
        'commentGroupId' : this.cgi,
        'parentId' : this.pi
      };

      this.addLayerComment.emit(data);
    }
  }
}
