import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {CommentComponent} from "../../components/comment/comment.component";
import {CommentListComponent} from "../../components/comment/comment-list/comment-list.component";
import {CommentFormComponent} from "../../components/comment/comment-form/comment-form.component";
import {ReactiveFormsModule} from "@angular/forms";
import {NgxPaginationModule} from "ngx-pagination";
import {CommentPaginationComponent} from "../../components/comment/comment-pagination/comment-pagination.component";


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    NgxPaginationModule
  ],
  declarations: [
    CommentComponent,
    CommentListComponent,
    CommentFormComponent,
    CommentPaginationComponent
  ],
  exports: [
    CommentComponent
  ]
})
export class CommentModule { }
