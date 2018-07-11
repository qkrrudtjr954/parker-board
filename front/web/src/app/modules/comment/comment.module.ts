import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {CommentComponent} from "../../components/comment/comment.component";
import {CommentListComponent} from "../../components/comment/comment-list/comment-list.component";
import {CommentFormComponent} from "../../components/comment/comment-form/comment-form.component";
import {ReactiveFormsModule} from "@angular/forms";
import {NgxPaginationModule} from "ngx-pagination";
import {PaginationComponent} from "../../components/pagination/pagination.component";
import {IconsModule} from "../../icons/icons.module";
import {LayerCommentFormComponent} from "../../components/comment/comment-list/layer-comment-form/layer-comment-form.component";
import {CommentUpdateComponent} from "../../components/comment/comment-list/comment-update/comment-update.component";
import {CommentDeleteComponent} from "../../components/comment/comment-list/comment-delete/comment-delete.component";



@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    IconsModule,
    NgxPaginationModule
  ],
  declarations: [
    CommentComponent,
    CommentListComponent,
    CommentFormComponent,
    PaginationComponent,
    LayerCommentFormComponent,
    CommentDeleteComponent,
    CommentUpdateComponent
  ],
  exports: [
    CommentComponent
  ]
})
export class CommentModule { }
