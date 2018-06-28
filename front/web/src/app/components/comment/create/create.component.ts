import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {
  commentForm = new FormGroup({
    content: new FormControl()
  });

  constructor(private fb: FormBuilder) { }

  ngOnInit() {
    this.createCommentForm()
  }

  createCommentForm() {
    this.commentForm = this.fb.group({
      content: ['', [Validators.minLength(10)]]
    })
  }

  onSubmit() {
    const content = this.commentForm.controls['content'].value


  }
}
