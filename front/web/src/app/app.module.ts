import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/layout/header/header.component';
import { FooterComponent } from './components/layout/footer/footer.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { LoginComponent } from './components/auth/login/login.component';
import { MainComponent } from "./components/main/main.component";
import { LogoutComponent } from './components/auth/logout/logout.component';

import { RouterModule, Routes } from "@angular/router";
import { ReactiveFormsModule } from '@angular/forms';
import { CookieService} from "ngx-cookie-service";
import { BoardCreateComponent } from './components/board/create/create.component';
import { PaginationComponent } from "./components/pagination/pagination.component";
import { EditComponent } from './components/board/edit/edit.component';
import { BoardDetailComponent } from './components/board/detail/detail.component';
import { PostDetailComponent } from './components/post/detail/detail.component';
import { SignupComponent } from './components/auth/signup/signup.component';


const routes: Routes = [{
  path: 'login',
  component: LoginComponent
},{
  path: 'signup',
  component: SignupComponent
},{
  path: '',
  component: MainComponent
},{
  path: 'boards/create',
  component: BoardCreateComponent
},{
  path: 'boards/:id/posts',
  component: BoardDetailComponent
},{
  path: 'boards/:id/update',
  component: EditComponent
},{
  path: 'posts/:id',
  component: PostDetailComponent
}];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    NavbarComponent,
    LoginComponent,
    MainComponent,
    LogoutComponent,
    BoardCreateComponent,
    PaginationComponent,
    EditComponent,
    PostDetailComponent,
    BoardDetailComponent,
    SignupComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
