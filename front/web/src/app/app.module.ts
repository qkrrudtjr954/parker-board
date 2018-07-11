import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from "@angular/router";
import { ReactiveFormsModule } from '@angular/forms';
import { NgxPaginationModule } from "ngx-pagination";

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/layout/header/header.component';
import { FooterComponent } from './components/layout/footer/footer.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { LoginComponent } from './components/auth/login/login.component';
import { MainComponent } from "./components/main/main.component";
import { LogoutComponent } from './components/auth/logout/logout.component';
import { SignupComponent } from './components/auth/signup/signup.component';

import { CookieService} from "ngx-cookie-service";
import { BoardCreateComponent } from './components/board/create/create.component';
import { BoardEditComponent } from './components/board/edit/edit.component';
import { PostListComponent } from './components/post/post-list/post-list.component';
import { PostDetailComponent } from './components/post/detail/detail.component';
import { PostCreateComponent } from './components/post/create/create.component';
import { PostUpdateComponent } from './components/post/post-update/post-update.component';
import { BoardDetailComponent } from './components/board/board-detail/board-detail.component';
import { PostLikeComponent } from './components/post/post-like/post-like.component';
import {IconsModule} from "./icons/icons.module";

import {CommentModule} from "./modules/comment/comment.module";


const routes: Routes = [{
  path: '',
  component: MainComponent
},{
  path: 'login',
  component: LoginComponent
},{
  path: 'signup',
  component: SignupComponent
},{
  path: 'boards/create',
  component: BoardCreateComponent
},{
  path: 'boards/:id/posts',
  component: PostListComponent
},{
  path: 'boards/:id/update',
  component: BoardEditComponent
},{
  path: 'boards/:id/posts/create',
  component: PostCreateComponent
},{
  path: 'posts/:id',
  component: PostDetailComponent
},{
  path: 'posts/:id/update',
  component: PostUpdateComponent
}];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    NavbarComponent,
    MainComponent,
    SignupComponent,
    LoginComponent,
    LogoutComponent,
    BoardCreateComponent,
    BoardEditComponent,
    PostDetailComponent,
    PostCreateComponent,
    PostUpdateComponent,
    PostListComponent,
    BoardDetailComponent,
    PostLikeComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    NgxPaginationModule,
    IconsModule,
    CommentModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
